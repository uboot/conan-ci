import docker
import os
import re
import string
import tarfile
import threading

from conanci.config import logger
from conanci.ssh import decode
from io import BytesIO
from queue import Empty, SimpleQueue


docker_image_pattern = ("(([a-z0-9\\.-]+(:[0-9]+)?/)?"
                        "[a-z0-9\\.-/]+)[:@]([a-z0-9\\.-]+)$")
build_package_dir = "conan_build_package"


def add_content_to_tar(tar, file_name, text_data):
    tarinfo = tarfile.TarInfo("{0}/{1}".format(build_package_dir, file_name))
    content = BytesIO(bytes(text_data, "utf-8"))
    tarinfo.size = len(content.getbuffer())
    tar.addfile(tarinfo, content)


def create_build_tar(build_os: str, parameters: dict):
    if build_os == "Linux":
        script_template_name = "build.sh.in"
    else:
        script_template_name = "build.ps1.in"
    script_name = script_template_name[:-3]

    # read and configure build script
    setup_file_path = os.path.join(os.path.dirname(__file__), script_template_name)
    with open(setup_file_path) as setup_template_file:
        template = string.Template(setup_template_file.read())
    script = template.substitute({**parameters, "build_package_dir": build_package_dir})

    # place into archive
    f = BytesIO()
    tar = tarfile.open(mode="w", fileobj=f, dereference=True)
    add_content_to_tar(tar, script_name, script)
    add_content_to_tar(tar, "id_rsa", decode(parameters["ssh_key"]))
    add_content_to_tar(tar, "known_hosts", decode(parameters["known_hosts"]))
    if "conan_settings" in parameters.keys() and parameters["conan_settings"]:
        add_content_to_tar(tar, "settings.yml", decode(parameters["conan_settings"]))
    tar.close()
    f.seek(0)
    return f


class Builder(object):
    def __init__(self, build_os, image):
        self.__client = docker.from_env()
        self.__image = image
        self.__build_os = build_os
        self.__container = None
        self.__container_logs = None
        self.__cancel_lock = threading.Lock()
        self.__cancelled = False
        self.__logs = SimpleQueue()

    def __enter__(self):
        return self

    def pull(self, parameters):
        m = re.match(docker_image_pattern, self.__image)
        if not m:
            raise Exception("The image '{0}' is not a valid "
                            "docker image name".format(self.__image))
        tag = m.group(4)
        repository = m.group(1)
        if tag == "local":
            logger.info("Do not pull local image '%s'", self.__image)
            return

        auth_config = None
        if parameters['docker_user']:
            auth_config = {
                "username": parameters['docker_user'],
                "password": parameters['docker_password']
            }

        logger.info("Pull docker image '%s'", self.__image)
        self.__client.images.pull(repository=repository, tag=tag, auth_config=auth_config)

    def setup(self, parameters):
        logger.info("Setup docker container")
        build_tar = create_build_tar(self.__build_os, parameters)

        # with open("build.tar", "wb") as f:
        #     f.write(build_tar.read())
        # build_tar.seek(0)

        if self.__build_os == "Linux":
            command = "sh /{0}/build.sh".format(build_package_dir)
        else:
            command = 'cmd /s /c "powershell -File C:\\{0}\\build.ps1"'.format(build_package_dir)

        self.__container = self.__client.containers.create(image=self.__image,
                                                           command=command)
        logger.info("Created docker container '%s'", self.__container.short_id)

        if self.__build_os == "Linux":
            build_data_dir = "/"
        else:
            build_data_dir = "C:\\"
        result = self.__container.put_archive(build_data_dir, data=build_tar)
        if not result:
            raise Exception("Failed to copy build files to container '{0}'"\
                            .format(self.__container.short_id))

    def run(self):
        with self.__cancel_lock:
            if self.__cancelled:
                logger.info("Build was cancelled")
                return
            logger.info("Start build in container '{0}'" \
                        .format(self.__container.short_id))
            self.__container.start()
            self.__container_logs = self.__container.logs(stream=True, follow=True)
        for bytes in self.__container_logs:
            line = bytes.decode("utf-8").strip('\n\r')
            logger.info(line)
            self.__logs.put(line)
        with self.__cancel_lock:
            self.__container_logs = None
            if self.__cancelled:
                logger.info("Build was cancelled")
                return

        result = self.__container.wait()
        if result.get("StatusCode"):
            raise Exception("Build in container '{0}' failed with status '{1}'".format(
                            self.__container.short_id, result.get("StatusCode")))

    def cancel(self):
        with self.__cancel_lock:
            logger.info("Cancel build")
            self.__cancelled = True
            if self.__container_logs:
                logger.info("Close logs")
                self.__container_logs.close()

    def __exit__(self, type, value, traceback):
        if not self.__container:
            return

        try:
            logger.info("Stop docker container '%s'", self.__container.short_id)
            self.__container.stop()
        except docker.errors.APIError:
            pass

        try:
            logger.info("Remove docker container '%s'", self.__container.short_id)
            self.__container.remove()
        except docker.errors.APIError:
            pass

    def get_log_lines(self):
        try:
            while True:
                yield self.__logs.get_nowait()
        except Empty:
            pass
