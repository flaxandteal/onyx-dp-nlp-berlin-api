import functools

from app.config import DATA_LOCATION
from berlin import load


@functools.lru_cache
def get_db(location: str = DATA_LOCATION):
    db = load(location)
    return db
