import sys
from datetime import datetime, timedelta
from app import __version__ as VERSION
from app.settings import BUILD_TIME, GIT_COMMIT

# Define the check statuses
OK = "OK"
WARNING = "WARNING"
ERROR = "ERROR"

MILLISECONDS = timedelta(milliseconds=1)


class Healthcheck:
    def __init__(self, status, checks, start_time: datetime):
        self.start_time = start_time

        formatted_build_time = datetime.fromtimestamp(int(BUILD_TIME))
        self.build_time = formatted_build_time.strftime('%Y-%m-%dT%H:%M:%S%z')
        git_commit = GIT_COMMIT

        self.status = status
        self.version = {
            "version": VERSION,
            "build_time": self.build_time,
            "git_commit": git_commit,
            "language": "python",
            "language_version": sys.version,
        }
        self.checks = checks

    def to_json(self):
        start_time = self.start_time.strftime('%Y-%m-%dT%H:%M:%S%z')
        response = {
            "status": self.status,
            "version": self.version,
            "uptime": self.get_uptime(),
            "start_time": start_time,
            "checks": self.checks,
        }

        return response

    def get_uptime(self):
        return int((datetime.now() - self.start_time) / MILLISECONDS)
