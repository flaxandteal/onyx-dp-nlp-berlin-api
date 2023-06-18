import functools

from berlin import load
from typing import Optional

from app.settings import DATA_LOCATION


@functools.lru_cache
def get_db(location: Optional[str] = None):
    db = load(location or DATA_LOCATION)
    return db
