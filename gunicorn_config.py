# https://til.codeinthehole.com/posts/how-to-get-gunicorn-to-log-as-json/

import datetime
import logging
import sys
from app.settings import settings

import json_log_formatter

class JsonRequestFormatter(json_log_formatter.JSONFormatter):
    def json_record(
        self,
        event: str,
        extra: dict[str, str | int | float],
        record: logging.LogRecord,
    ) -> dict[str, str | int | float]:
        # Convert the log record to a JSON object.
        # See https://docs.gunicorn.org/en/stable/settings.html#access-log-format

        response_time = datetime.datetime.strptime(
            record.args["t"], "[%d/%b/%Y:%H:%M:%S %z]"
        )
        url = record.args["U"]
        if record.args["q"]:
            url += f"?{record.args['q']}"

        severity = 0 if record.levelname == "INFO" else 1 if record.levelname == "ERROR" else 2

        return dict(
            namespace=settings.NAMESPACE,
            remote_ip=record.args["h"],
            method=record.args["m"],
            event="making request",
            path=url,
            status=str(record.args["s"]),
            created_at=response_time.isoformat(),
            user_agent=record.args["a"],
            referer=record.args["f"],
            duration_in_ms=record.args["M"],
            pid=record.args["p"],
            severity=severity,
        )


class JsonErrorFormatter(json_log_formatter.JSONFormatter):
    def json_record(
        self,
        event: str,
        extra: dict[str, str | int | float],
        record: logging.LogRecord,
    ) -> dict[str, str | int | float]:
        payload: dict[str, str | int | float] = super().json_record(
            event, extra, record
        )
        payload["namespace"] = settings.NAMESPACE
        payload["created_at"] = payload["time"]
        payload["event"] = record.getMessage()
        payload["level"] = record.levelname
        payload["severity"] = 0 if record.levelname == "INFO" else 1 if record.levelname == "ERROR" else 2
        payload.pop('time', None)
        payload.pop('message', None)

        return payload


# Ensure the two named loggers that Gunicorn uses are configured to use a custom
# JSON formatter.
logconfig_dict = {
    "version": 1,
    "formatters": {
        "json_request": {
            "()": JsonRequestFormatter,
        },
        "json_error": {
            "()": JsonErrorFormatter,
        },
    },
    "handlers": {
        "json_request": {
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter": "json_request",
        },
        "json_error": {
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter": "json_error",
        },
    },
    "root": {"level": "INFO", "handlers": []},
    "loggers": {
        "gunicorn.access": {
            "level": "INFO",
            "handlers": ["json_request"],
            "propagate": False,
        },
        "gunicorn.error": {
            "level": "INFO",
            "handlers": ["json_error"],
            "propagate": False,
        },
    },
}
