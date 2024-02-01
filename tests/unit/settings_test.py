from unittest.mock import patch

import pytest


@pytest.fixture
def mock_settings():
    with patch("app.settings.settings") as mock_settings:
        mock_settings.HOST = "mock_host"
        mock_settings.PORT = 8080
        mock_settings.NAMESPACE = "mock_namespace"
        mock_settings.DATA_LOCATION = "/path/to/data"
        mock_settings.BUILD_TIME = 1234567890
        mock_settings.GIT_COMMIT = "mock_commit"
        yield mock_settings

def test_settings(mock_settings):
    assert mock_settings.HOST == "mock_host"
    assert mock_settings.PORT == 8080
    assert mock_settings.NAMESPACE == "mock_namespace"
    assert mock_settings.DATA_LOCATION == "/path/to/data"
    assert mock_settings.BUILD_TIME == 1234567890
    assert mock_settings.GIT_COMMIT == "mock_commit"
