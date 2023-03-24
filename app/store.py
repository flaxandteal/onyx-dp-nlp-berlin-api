import functools
import berlin

@functools.cache
def get_db(location: str = "data"):
    db = berlin.load(location)
    return db
