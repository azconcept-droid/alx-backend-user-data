#!/usr/bin/env python3
"""
Log filter
"""
from typing import List
import re
import logging


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self._fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Format log record """
        message = filter_datum(self._fields, self.REDACTION,
                               super().format(record), self.SEPARATOR)
        return message


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """returns log message obfuscated """
    for field in fields:
        replacement = field + "=" + redaction + separator
        message = re.sub(field + "=.*?" + separator, replacement, message)
    return message


def get_logger() -> logging.Logger:
    """ Get logger """
    logger = logging.getLogger("user_data")

    logger.setLevel(logging.INFO)
    logger.propagate = False

    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))

    logger.addHandler(handler)

    return logger
