import functools
from typing import Optional

from berlin import load

from app.settings import settings


@functools.lru_cache
def get_db(location: Optional[str] = None):
    db = load(location or settings.DATA_LOCATION)
    return db
