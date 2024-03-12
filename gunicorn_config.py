# https://til.codeinthehole.com/posts/how-to-get-gunicorn-to-log-as-json/

import datetime
import logging
import sys

import json_log_formatter

from app.settings import settings

import re

def format_stack_trace(stack_trace):
    # Split the stack trace into lines removing caret chars
    lines = ''.join(stack_trace.split()).replace('^', '')

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
            "line": ''.join(line_number.split("line")),
        }
        
        formatted_stack_trace.append(formatted_entry)
    
    return formatted_stack_trace

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
        colon_index = record.args["{host}i"].find(':')
        port = record.args["{host}i"][colon_index + 1:].strip()
        payload["namespace"] = settings.NAMESPACE
        payload["created_at"] = payload["time"].isoformat(timespec="milliseconds") + "Z"
        payload["event"] = "making request"
        payload["http"] = {
            "method": record.args["m"],
            "scheme": record.args["H"],
            "host": record.args["h"],
            "port": port,
            "path": record.args["U"],
            "query": record.args["q"],
            "status_code": record.args["s"],
            "started_at": payload["time"].isoformat(timespec="milliseconds") + "Z",
        }

        if record.args["s"] != "200":
            payload["severity"] = 1
            payload["error"]= [
                {
                    "message": "received non-200 status code"
                }
            ]
        else:
            payload["severity"] = 3

        # Remove unnecessary default fields
        payload.pop("time", None)
        payload.pop("taskName", None)
        payload.pop("message", None)

        return payload

class JsonServerFormatter(json_log_formatter.JSONFormatter):
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
        payload["created_at"] = payload["time"].isoformat(timespec="milliseconds") + "Z"

        if record.levelname == "ERROR":
            payload["event"] = "gunicorn has experienced an error"
            payload["errors"] = [
                {
                    "message": record.getMessage(),
                    "data": {
                        "level": record.levelname
                    }
                }
            ]

            if "exc_info" in payload:
                formatted_stack_trace = format_stack_trace(payload["exc_info"])
                payload["errors"][0]["error"] = formatted_stack_trace

            payload["severity"] = 1
        else:
            payload["event"] = record.getMessage()
            payload["severity"] = 3

        payload.pop("time", None)
        payload.pop("exc_info", None)
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
        "json_server": {
            "()": JsonServerFormatter,
        },
    },
    "handlers": {
        "json_request": {
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter": "json_request",
        },
        "json_server": {
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter": "json_server",
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
            "handlers": ["json_server"],
            "propagate": False,
        },
    },
}

bind = f"0.0.0.0:{settings.PORT}"

