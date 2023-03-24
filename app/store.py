import functools
from berlin import load

@functools.cache
def get_db(location: str = "data"):
    db = load(location)
    return db
