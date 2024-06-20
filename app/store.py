import functools
import traceback
from typing import Optional

from berlin import load

from app.logger import format_errors, logger
from app.settings import settings


@functools.lru_cache
def get_db(location: Optional[str] = None):
    try:
        db = load(location or settings.DATA_LOCATION)
        return db
    except Exception as e:
        logger.error(
            event="unable to load database",
            errors=format_errors(e, trace=traceback.format_exc()),
        )
