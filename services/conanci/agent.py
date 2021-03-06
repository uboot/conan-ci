from conanci import database
from conanci.builder import Builder
from conanci.config import connect_to_database, logger
from conanci.worker import Worker
from sqlalchemy import func, update
import asyncio
import os


conanci_os = os.environ.get("CONANCI_AGENT_OS", "Linux")


async def _run_build(builder, parameters):
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, builder.pull, parameters)
    await loop.run_in_executor(None, builder.setup, parameters)
    await loop.run_in_executor(None, builder.run)


class Agent(Worker):
    def __init__(self):
        super().__init__()
        connect_to_database()
        self.__build_id = None

    async def work(self):
        new_builds = True
        while new_builds:
            try:
                new_builds = await self.__process_builds()
            except Exception as e:
                logger.error("Processing builds failed: %s", e)

    async def __process_builds(self):
        # database.populate_database()
        # return
        logger.info("Start processing builds")
        with database.session_scope() as session:
            build = session\
                .query(database.Build)\
                .join(database.Build.profile).join(database.Profile.settings)\
                .filter(database.Setting.key=='os',\
                    database.Setting.value==conanci_os,\
                    database.Build.status==database.BuildStatus.new)\
                .populate_existing()\
                .with_for_update(skip_locked=True, of=database.Build)\
                .first()

            if not build:
                logger.info("Stop processing builds with *no* builds processed")
                return False
        
            logger.info("Set status of build '%d' to 'active'", build.id)
            self.__build_id = build.id
            build.status = database.BuildStatus.active
            build.log = database.Log()
            build.log.logs = ''

            container = build.profile.container
            parameters = {
                "conan_remote": build.profile.ecosystem.conan_remote,
                "conan_verify_ssl": build.profile.ecosystem.conan_verify_ssl,
                "conan_user": build.profile.ecosystem.conan_user,
                "conan_password": build.profile.ecosystem.conan_password,
                "conan_settings": build.profile.ecosystem.settings,
                "git_url": build.commit.repo.url,
                "git_sha": build.commit.sha,
                "conanci_user": build.profile.ecosystem.user,
                "conan_args": " ".join(["-s {0}={1}".format(setting.key, setting.value)
                                        for setting in build.profile.settings]),
                "channel": build.commit.channel.name,
                "path": os.path.join(build.commit.repo.path, "conanfile.py")
                        if build.commit.repo.path != "" else "conanfile.py",
                "ssh_key": build.profile.ecosystem.ssh_key,
                "known_hosts": build.profile.ecosystem.known_hosts,
                "docker_user": build.profile.docker_user,
                "docker_password": build.profile.docker_password
            }

        try:
            with Builder(conanci_os, container) as builder:
                builder_task = asyncio.create_task(_run_build(builder, parameters))
                while True:
                    # wait 10 seconds
                    done, _ = await asyncio.wait({builder_task}, timeout=10)
                    self.__update_logs(builder)

                    # if finished exit
                    if done:
                        builder_task.result()
                        break

                    # check if the build was stopped and cancel it
                    # if necessary
                    if self.__cancel_stopping_build(builder):
                        return True

                logger.info("Set status of build '%d' to 'success'", self.__build_id)
                self.__set_build_status(database.BuildStatus.success)
                self.__build_id = None
        except Exception as e:
            logger.error(e)
            logger.info("Set status of build '%d' to 'error'", self.__build_id)
            self.__set_build_status(database.BuildStatus.error)
            self.__build_id = None
            
        return True

    def cleanup(self):
        if not self.__build_id:
            return

        logger.info("Set status of build '%d' to 'new'", self.__build_id)
        self.__set_build_status(database.BuildStatus.new)

    def __set_build_status(self, status):
        if not self.__build_id:
            return

        with database.session_scope() as session:
            build = session.query(database.Build) \
                .filter_by(id=self.__build_id) \
                .first()
            if build:
                build.status = status
                self.__build_id = None
            else:
                logger.error("Failed to find build '%d' in database", self.__build_id)

    def __update_logs(self, builder):
        with database.session_scope() as session:
            build = session.query(database.Build) \
                .filter_by(id=self.__build_id) \
                .first()

            if not build:
                return

            log_lines = [line for line in builder.get_log_lines()]
            log_tail = '\n' + '\n'.join(log_lines)
            statement = update(database.Log) \
                .where(database.Log.id == build.log_id) \
                .values(logs=func.concat(database.Log.logs, log_tail))
            session.execute(statement)

    def __cancel_stopping_build(self, builder):
        with database.session_scope() as session:
            build = session.query(database.Build) \
                .filter_by(id=self.__build_id, status=database.BuildStatus.stopping) \
                .first()
            if not build:
                return False

            logger.info("Cancel build '%d'", self.__build_id)
            builder.cancel()
            logger.info("Set status of build '%d' to 'stopped'", self.__build_id)
            build.status = database.BuildStatus.stopped
            self.__build_id = None
            return True

