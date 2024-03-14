# https://til.codeinthehole.com/posts/how-to-get-gunicorn-to-log-as-json/

import logging
import sys
from datetime import datetime

import json_log_formatter

from app.settings import settings


def format_stack_trace(stack_trace):
    # Split the stack trace into lines removing caret chars
    lines = "".join(stack_trace.split()).replace("^", "")

    # Split by File as there's always 1 file per entry
    lines = lines.split("File")

    # Remove first entry as it's always Traceback(mostrecentcalllast)
    lines = lines[1:]

    # Initialize an empty list to store formatted stack trace entries
    formatted_stack_trace = []

    # Iterate through each line in the stack trace
    for line in lines:
        # split by "," to separate file_path, line_number, function_name
        line = line.split(",")
        file_path, line_number, function_name = line[0], line[1], line[2]

        formatted_entry = {
            "file": file_path,
            "function": function_name,
            "line": "".join(line_number.split("line")),
        }

        formatted_stack_trace.append(formatted_entry)

    return formatted_stack_trace


class SuppressInfoFilter(logging.Filter):
    def filter(self, record):
        return record.levelno != logging.INFO or record.name != "gunicorn.error"


class SuppressErrorFilter(logging.Filter):
    def filter(self, record):
        return record.levelno != logging.ERROR or record.name != "gunicorn.error"


class JsonRequestFormatter(json_log_formatter.JSONFormatter):
    def json_record(
        self,
        event: str,
        extra: dict[str, str | int | float],
        record: logging.LogRecord,
    ) -> dict[str, str | int | float]:
        payload: dict[str, str | int | float] = super().json_record(
            event, extra, record
        )
        colon_index = record.args["{host}i"].find(":")
        port = record.args["{host}i"][colon_index + 1 :].strip()

        payload["namespace"] = settings.NAMESPACE
        payload["created_at"] = (
            datetime.utcnow().isoformat(timespec="milliseconds") + "Z"
        )
        payload["event"] = "http request received"
        payload["severity"] = 3
        payload["http"] = {
            "method": record.args["m"],
            "scheme": record.args["H"],
            "host": record.args["h"],
            "port": port,
            "path": record.args["U"],
            "query": record.args["q"],
            "status_code": record.args["s"],
            "started_at": datetime.utcnow().isoformat(timespec="milliseconds") + "Z",
        }

        # Remove unnecessary default fields
        payload.pop("time", None)
        payload.pop("taskName", None)
        payload.pop("message", None)

        return payload


class JsonServerInfoFormatter(json_log_formatter.JSONFormatter):
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
        payload["created_at"] = (
            datetime.utcnow().isoformat(timespec="milliseconds") + "Z"
        )
        payload["event"] = record.getMessage()
        payload["severity"] = 3

        payload.pop("time", None)
        payload.pop("exc_info", None)
        payload.pop("taskName", None)
        payload.pop("message", None)

        return payload


class JsonServerErrorFormatter(json_log_formatter.JSONFormatter):
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
        payload["created_at"] = (
            datetime.utcnow().isoformat(timespec="milliseconds") + "Z"
        )
        payload["severity"] = 1

        payload["event"] = "server has experienced an error"
        payload["errors"] = [
            {
                "message": record.getMessage(),
            }
        ]

        if "exc_info" in payload:
            formatted_stack_trace = format_stack_trace(payload["exc_info"])
            payload["errors"][0]["error"] = formatted_stack_trace

        payload.pop("time", None)
        payload.pop("exc_info", None)
        payload.pop("taskName", None)
        payload.pop("message", None)

        return payload


class JsonServerErrorHandler(logging.StreamHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stream = sys.stderr
        self.setFormatter(JsonServerErrorFormatter())
        self.addFilter(SuppressInfoFilter())

class JsonServerInfoHandler(logging.StreamHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stream = sys.stdout
        self.setFormatter(JsonServerInfoFormatter())
        self.addFilter(SuppressErrorFilter())

# Ensure the two named loggers that Gunicorn uses are configured to use a custom
# JSON formatter.
logconfig_dict = {
    "version": 1,
    "formatters": {
        "json_server_error": {
            "()": JsonServerErrorFormatter,
        },
        "json_request": {
            "()": JsonRequestFormatter,
        },
        "json_server_info": {
            "()": JsonServerInfoFormatter,
        },
    },
    "handlers": {
        "json_server_error": {
            "class": "gunicorn_config.JsonServerErrorHandler",
            "stream": sys.stderr,
            "formatter": "json_server_error",
        },
        "json_request": {
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter": "json_request",
        },
        "json_server_info": {
            "class": "gunicorn_config.JsonServerInfoHandler",
            "stream": sys.stdout,
            "formatter": "json_server_info",
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
            "handlers": ["json_server_info", "json_server_error"],
            "propagate": False,
        },
    },
}

bind = f"0.0.0.0:{settings.PORT}"
