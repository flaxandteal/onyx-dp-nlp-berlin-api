import logging
import logging.config
from datetime import datetime

import structlog
import structlog._log_levels

from app.settings import settings
from gunicorn_config import format_stack_trace


def add_severity_level(logger, method_name, event_dict):
    if method_name == "info":
        event_dict[0][0]["severity"] = 3
    elif method_name == "error":
        event_dict[0][0]["severity"] = 1

    return event_dict


def format_errors(*excs: BaseException, trace=None):
    errors = []

    for exc in excs:
        error = {
            "message": str(exc),
        }
        if trace:
            error["error"] = format_stack_trace(trace)

        errors.append(error)

    return errors


def setup_logging():
    shared_processors = []
    processors = shared_processors + [
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        add_severity_level,
    ]
    structlog.configure(
        cache_logger_on_first_use=True,
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        processors=processors,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
    )

    stdlib_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "json": {
                "()": structlog.stdlib.ProcessorFormatter,
                "processor": structlog.processors.JSONRenderer(),
                "foreign_pre_chain": shared_processors,
            },
        },
        "handlers": {
            "stream": {
                "level": "DEBUG",
                "formatter": "json",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stderr",
            },
        },
        "loggers": {
            "": {
                "handlers": ["stream"],
                "level": "DEBUG",
                "propagate": True,
            },
        },
    }
    logging.config.dictConfig(stdlib_config)

    return structlog.get_logger(
        namespace=settings.NAMESPACE,
        created_at=datetime.utcnow().isoformat(timespec="milliseconds") + "Z",
        event="",
        severity=3,  # default
    )


logger = setup_logging()
