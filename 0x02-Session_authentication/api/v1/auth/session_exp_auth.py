#!/usr/bin/env python3
""" Session Expiration module
"""
from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """ Session expiration class """
    def __init__(self) -> None:
        """ Initialize session exp auth class """
        try:
            self.session_duration = int(getenv('SESSION_DURATION'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """ create new session """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        self.user_id_by_session_id[session_id] = {}
        self.user_id_by_session_id[session_id]['user_id'] = user_id
        self.user_id_by_session_id[session_id]['created_at'] = datetime.now()

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ return user_id for session id """
        if session_id is None:
            return None
        new_session_dict = self.user_id_by_session_id.get(session_id)
        user_id = new_session_dict.get('user_id')
        if user_id is None:
            return None
        if self.session_duration <= 0:
            return user_id
        created_at = new_session_dict.get('created_at')
        if created_at is None:
            return None
        expr_time = created_at + timedelta(seconds=self.session_duration)

        if datetime.now() > expr_time:
            return None
        return user_id
