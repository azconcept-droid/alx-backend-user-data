#!/usr/bin/env python3
"""Authentication module
"""
import bcrypt
import uuid
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register authenticated user"""
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError('User {} already exists'.format(email))
        except NoResultFound:
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password)

            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """login registered user"""
        try:
            user = self._db.find_user_by(email=email)
            passwd = password.encode('utf-8')
            if bcrypt.checkpw(passwd, user.hashed_password):
                return True
            else:
                return False
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None


def _hash_password(password: str) -> bytes:
    """hash user password"""
    passwd = password.encode('utf-8')

    salt = bcrypt.gensalt()

    return bcrypt.hashpw(passwd, salt)


def _generate_uuid() -> str:
    """Generate uuid"""
    return str(uuid.uuid4())
