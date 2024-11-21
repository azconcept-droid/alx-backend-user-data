#!/usr/bin/env python3
"""Authentication module
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """hash user password"""
    passwd = password.encode('utf-8')

    salt = bcrypt.gensalt()

    return bcrypt.hashpw(passwd, salt)
