import pytest
from unittest.mock import patch
from api import create_app
from dataclasses import dataclass
import app.store

def fake_berlin_load(location):
    @dataclass
    class FakeBerlinResult:
        key: str
        encoding: str
        id: str
        words: list[str]

    class FakeBerlinDbProxy:
        def query(self, query, state, limit, lev_distance):
            return [FakeBerlinResult("A", "B", "X", ["Manchester"])]

    assert location == "data"
    return FakeBerlinDbProxy()

@pytest.fixture()
def app():
    with patch("app.store.load", fake_berlin_load):
        app = create_app()
        app.config.update({
            "TESTING": True,
        })

        yield app

@pytest.fixture()
def test_client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
