# https://til.codeinthehole.com/posts/how-to-get-gunicorn-to-log-as-json/

import datetime
import logging
import sys

import json_log_formatter

from app.settings import settings


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
        if "?" in url:
            path, query = url.split("?", 1)
        else:
            path = url
            query = ""
        if record.args["q"]:
            url += f"?{record.args['q']}"

        severity = (
            3 if record.levelname == "INFO" else 1 if record.levelname == "ERROR" else 0
        )

        return dict(
            namespace=settings.NAMESPACE,
            event="making request",
            created_at=response_time.isoformat(timespec="milliseconds") + "Z",
            data={
                "remote_ip": record.args["h"],
                "status": str(record.args["s"]),
            },
            method=record.args["m"],
            path=path,
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
        payload["created_at"] = payload["time"].isoformat(timespec="milliseconds") + "Z",
        payload["errors"] = [
            {
                "message": event,
                "data": {
                    "level": record.levelname
                }
            }
        ]
        try:
            exc = extra["exc"]
            stack_trace = traceback.extract_tb(exc.__traceback__).format()
            payload["errors"][0]["stack_trace"] = stack_trace
        except:
            ...

        payload["severity"] = (
            3 if record.levelname == "INFO" else 1 if record.levelname == "ERROR" else 0
        )
        payload.pop("time", None)
        payload.pop("taskName", None)
        payload.pop("message", None)

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

bind = f"0.0.0.0:{settings.PORT}"
