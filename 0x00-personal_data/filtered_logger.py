#!/usr/bin/env python3
"""
Log filter
"""
from typing import List
import re


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """returns log message obfuscated """
    for field in fields:
        replacement = field + "=" + redaction + separator
        message = re.sub(field + "=.*?" + separator, replacement, message)
    return message
