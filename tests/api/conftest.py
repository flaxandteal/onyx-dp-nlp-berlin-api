import importlib
import json
from dataclasses import dataclass
from unittest.mock import patch

import pytest

from app.main import create_app
from app.store import get_db


def load_test_code_list():
    return [
        {
            "change": "",
            "country": "BG",
            "subcode": "BLO",
            "name": "Lyuliakovo",
            "name_wo_diacritics": "Lyuliakovo",
            "subdivision_code": "02",
            "status": "RL",
            "function": "-----6--",
            "date": "0901",
            "iata_code": "",
            "coordinates": "4283N 02701E",
        }
    ]


def load_test_codes():
    return [
        json.dumps(
            {
                "BG": {
                    "<c>": "ISO-3166-1",
                    "s": '<bln|ISO-3166-1#BG|"Bulgaria">',
                    "i": "BG",
                    "d": {
                        "name": "Bulgaria",
                        "short": "Bulgaria",
                        "alpha2": "BG",
                        "alpha3": "BGR",
                        "official_en": "Bulgaria",
                        "official_fr": "Bulgarie",
                        "continent": "EU",
                    },
                },
                "BG:02": {
                    "<c>": "ISO-3166-2",
                    "s": "<bln|ISO-3166-2#BG:02|\"Burgas\">",
                    "i": "BG:02",
                    "d": {
                        "name": "Burgas",
                        "supercode": "BG",
                        "subcode": "02",
                        "level": "region"
                    }
                },
                "BG:BLO": {
                    "<c>": "UN-LOCODE",
                    "s": '<bln|UN-LOCODE#BG:BLO|"Lyuliakovo">',
                    "i": "BG:BLO",
                    "d": {
                        "name": "Lyuliakovo",
                        "supercode": "BG",
                        "subcode": "BLO",
                        "subdivision_name": "Burgas",
                        "subdivision_code": "02",
                        "function_code": "-----6--",
                    },
                },
            }
        )
    ]


def real_berlin_load(location):
    import berlin

    db = berlin.load_from_json([load_test_codes()], load_test_code_list())
    db.retrieve("UN-LOCODE-bg:blo")
    return db


def fake_berlin_load(location):
    @dataclass
    class FakeBerlinResult:
        key: str
        encoding: str
        id: str
        words: list[str]

        def get_names(self):
            return ["manc"]

        def get_codes(self):
            return ["mnc"]

        def get_subdiv_code(self):
            return "mac"

        def get_state_code(self):
            return "gb"
        
        def get_score(self):
            return 1010 
        
        def get_offset(self):
            return [0, 10]
        

    class FakeBerlinDbProxy:
        def query(self, query, state, limit, lev_distance):
            return [FakeBerlinResult("A", "B", "X", ["Manchester"])]

        def get_subdiv_key(self, state, subdiv):
            return f"{state}-{subdiv}-name"

        def get_state_key(self, state):
            return f"{state}-nom"

    assert location == "data/"
    return FakeBerlinDbProxy()


@pytest.fixture()
def app_with_berlin():
    with patch("app.store.load", real_berlin_load):
        import app.views.berlin

        importlib.reload(app.views.berlin)
        get_db.cache_clear()

        app = create_app()
        app.config.update(
            {
                "TESTING": True,
            }
        )

        yield app


@pytest.fixture()
def app():
    with patch("app.store.load", fake_berlin_load):
        import app.views.berlin

        importlib.reload(app.views.berlin)
        get_db.cache_clear()

        app = create_app()
        app.config.update(
            {
                "TESTING": True,
            }
        )

        yield app


@pytest.fixture()
def test_client_with_berlin(app_with_berlin):
    yield app_with_berlin.test_client()


@pytest.fixture()
def test_client(app):
    yield app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
