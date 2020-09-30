from swagger_server.config import app, db
from swagger_server import database
import git
import os.path
import re
import shutil

data_dir = os.environ.get("CRAWLER_REPO_DIR", "/data")
logger = app.app.logger


class RepoController(object):
    def __init__(self, repo_dir):
        self.repo_dir = repo_dir

    def is_clone_of(self, url):
        try:
            repo = git.Repo(self.repo_dir)
        except git.exc.NoSuchPathError:
            return False

        if len(repo.remotes) == 0:
            return False

        for remote_url in repo.remotes[0].urls:
            if remote_url == url:
                return True
        return False

    def create_new_clone(self, url):
        shutil.rmtree(self.repo_dir, ignore_errors=True)
        git.Repo.clone_from(url=url, to_path=self.repo_dir)

    def fetch(self):
        repo = git.Repo(self.repo_dir)
        repo.git.fetch()

    def get_remote_branches(self):
        repo = git.Repo(self.repo_dir)
        branches = [b.strip() for b in repo.git.branch('-r').split()]
        pattern = 'origin/([/\\-\\w]+)'
        matches = [re.match(pattern, b) for b in branches]
        return list(set(m.group(1) for m in matches
                    if m and m.group(1) != 'HEAD'))

    def checkout(self, branch):
        repo = git.Repo(self.repo_dir)
        repo.git.reset('--hard', 'origin/{}'.format(branch))

    def get_sha(self):
        repo = git.Repo(self.repo_dir)
        return repo.head.commit.hexsha


def run():
    logger.info("start crawling")

    if not os.path.exists(data_dir):
        os.makedirs(data_dir, exist_ok=True)
        logger.info("created directory '%s'", data_dir)

    repos = database.Repo.query.all()
    channels = database.Channel.query.all()
    for repo in repos:
        repo_dir = os.path.join(data_dir, str(repo.id))
        controller = RepoController(repo_dir)
        if not controller.is_clone_of(repo.url):
            logger.info("clone URL '%s' to '%s'", repo.url, repo_dir)
            controller.create_new_clone(repo.url)
        else:
            logger.info("fetch existing repo '%s' for URL '%s'",
                        repo_dir, repo.url)
            controller.fetch()

        branches = controller.get_remote_branches()
        for channel in channels:
            if channel.branch in branches:
                logger.info("checkout branch '%s'", channel.branch)
                controller.checkout(channel.branch)
                sha = controller.get_sha()

                commits = database.Commit.query.filter_by(repo=repo, sha=sha,
                                                          channel=channel)

                # continue if this commit has already been stored
                if list(commits):
                    logger.info("commit '%s' exists", sha[:7])
                    continue

                logger.info("add commit '%s'", sha[:7])
                commit = database.Commit()
                commit.sha = sha
                commit.repo = repo
                commit.channel = channel
                commit.status = database.CommitStatus.new
                db.session.add(commit)

                old_commits = database.Commit.query.filter(
                    database.Commit.repo == repo,
                    database.Commit.channel == channel,
                    database.Commit.sha != sha,
                    database.Commit.status != database.CommitStatus.old
                )
                for c in old_commits:
                    logger.info("set status of '%s' to 'old'", c.sha[:7])
                    c.status = database.CommitStatus.old
                db.session.commit()
