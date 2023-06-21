import sys
from datetime import datetime, timedelta
from unittest.mock import patch

import pytest

from app import __version__ as VERSION
from app.settings import settings
from app.healthcheck import Healthcheck, OK

start_time = datetime.now()


@pytest.fixture
def healthcheck():
    checks = {"check1": OK, "check2": OK}
    return Healthcheck(OK, checks, start_time)


@patch("app.healthcheck.datetime")
def test_to_json(mock_datetime, healthcheck):
    formatted_build_time = datetime.fromtimestamp(int(settings.BUILD_TIME))
    build_time = formatted_build_time.strftime('%Y-%m-%dT%H:%M:%S%z')

    expected_json = {
        "status": OK,
        "version": {
            "version": VERSION,
            "build_time": build_time,
            "git_commit": settings.GIT_COMMIT,
            "language": "python",
            "language_version": sys.version,
        },
        "uptime": 1,
        "start_time": start_time.strftime('%Y-%m-%dT%H:%M:%S%z'),
        "checks": {"check1": OK, "check2": OK},
    }

    result = healthcheck.to_json()
    print ("this is: ", result)
    print ("this is: ", expected_json)

    assert result == expected_json


@patch("app.healthcheck.datetime")
def test_get_uptime(mock_datetime, healthcheck):
    mock_datetime.now.return_value = healthcheck.start_time + timedelta(milliseconds=500)

    result = healthcheck.get_uptime()

    assert result == 500
