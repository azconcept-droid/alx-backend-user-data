#!/usr/bin/env python3
"""
Log filter
"""
from typing import List
import re
import logging


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
