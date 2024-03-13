import logging.config
import sys
import unittest

from datetime import datetime
from io import StringIO
from unittest.mock import patch
from gunicorn_config import (JsonRequestFormatter, JsonServerErrorFormatter,
                             JsonServerInfoFormatter, logconfig_dict)


class TestLogFormatting(unittest.TestCase):
    def setUp(self):
        logging.config.dictConfig(logconfig_dict)

    def test_request_formatting(self):
        record = logging.LogRecord(
            name="gunicorn.access",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg="Log message",
            args={
                "h": "127.0.0.1",
                "U": "/path/to/resource",
                "m": "GET",
                "s": "200",
                "q": "param=value",
                "H": "https",
                "{host}i": "1234"
                
            },
            exc_info=None,
        )

        stream_buffer = StringIO()

        with patch("sys.stdout", stream_buffer):
            formatter = JsonRequestFormatter()
            formatted_log = formatter.json_record(event="testing request logs", extra={}, record=record)

            expected={
                'namespace': 'dp-nlp-berlin-api', 
                'event': 'making request', 
                'http': {
                    'method': 'GET', 
                    'scheme': 'https', 
                    'host': '127.0.0.1',
                    'port': '1234',
                    'path': '/path/to/resource',
                    'query': 'param=value', 
                    'status_code': '200',
                }, 
                'severity': 3
            }


            # Default required logs 
            self.assertEqual(expected["namespace"], formatted_log["namespace"])
            self.assertEqual(expected["event"], formatted_log["event"])
            self.assertEqual(expected["severity"], formatted_log["severity"])

            # Http logs 
            self.assertEqual(expected["http"]["method"], formatted_log["http"]["method"])
            self.assertEqual(expected["http"]["scheme"], formatted_log["http"]["scheme"])
            self.assertEqual(expected["http"]["host"], formatted_log["http"]["host"])
            self.assertEqual(expected["http"]["port"], formatted_log["http"]["port"])
            self.assertEqual(expected["http"]["path"], formatted_log["http"]["path"])
            self.assertEqual(expected["http"]["query"], formatted_log["http"]["query"])
            self.assertTrue(parsable_isoformat(time=formatted_log["http"]["started_at"]))
            self.assertTrue(parsable_isoformat(formatted_log["created_at"]))

    def test_server_log_formatting(self):
        record = logging.LogRecord(
            name="gunicorn.error",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg="server starting",
            args=(),
            exc_info=None,
        )
        stream_buffer = StringIO()

        with patch("sys.stdout", stream_buffer):
            formatter = JsonServerInfoFormatter()
            formatted_log = formatter.json_record(event="testing server logs", extra={}, record=record)

            expected={
                'namespace': 'dp-nlp-berlin-api', 
                'event': 'server starting', 
                'severity': 3
            }

            self.assertEqual(expected["namespace"], formatted_log["namespace"])
            self.assertEqual(expected["event"], formatted_log["event"])
            self.assertEqual(expected["severity"], formatted_log["severity"])
            self.assertTrue(parsable_isoformat(formatted_log["created_at"]))

    def test_server_error_formatting(self):
        try:
            # This will raise a NameError
            nonexistent_variable # noqa
        except Exception:
            # Capture the exception information to use as actual traceback for the logging
            exc_info = sys.exc_info()

            record = logging.LogRecord(
                name="gunicorn.error",
                level=logging.ERROR,
                pathname="",
                lineno=0,
                msg="specific err msg",
                args=(),
                exc_info=exc_info,
            )

            stream_buffer = StringIO()

            with patch("sys.stderr", stream_buffer):
                formatter = JsonServerErrorFormatter()
                formatted_log = formatter.json_record(event="testing server logs", extra={}, record=record)

                expected={
                    'namespace': 'dp-nlp-berlin-api', 
                    'created_at': '2024-03-11T15:50:52.180+00:00Z', 
                    'event': 'server has experienced an error',
                    'errors': [
                        {
                            "message": 'specific err msg',
                        }
                    ],
                    'severity': 1
                }

                # Default required logs 
                self.assertEqual(expected["namespace"], formatted_log["namespace"])
                self.assertEqual(expected["event"], formatted_log["event"])
                self.assertEqual(expected["severity"], formatted_log["severity"])

                # Error logs 
                self.assertEqual(expected["errors"][0]["message"], formatted_log["errors"][0]["message"])
                assert "/gunicorn_test.py" in formatted_log["errors"][0]["error"][0]["file"]
                assert "nonexistent_variable" in formatted_log["errors"][0]["error"][0]["function"]
                assert formatted_log["errors"][0]["error"][0]["line"]
            
def parsable_isoformat(time):
    desired_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    try:
        _ = datetime.strptime(time, desired_format)
        return True  # If parsing succeeds, the format is correct
    except ValueError:
        return False, "Invalid format"

if __name__ == "__main__":
    unittest.main()
