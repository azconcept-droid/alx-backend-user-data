#!/usr/bin/env python3
""" Session database auth module
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from os import getenv


class SessionDBAuth(SessionExpAuth):
    """ Session db auth class
    """
    def create_session(self, user_id=None):
        """ create new session """
        self.user_session = UserSession()
        self.user_session.user_id = user_id
        return self.user_session.session_id

    def user_id_for_session_id(self, session_id=None):
        """ return user id for that session"""
        if self.user_session.session_id == session_id:
            return self.user_session.user_id

    def destroy_session(self, request=None):
        """ cancle user session """
        session_name = getenv("SESSION_NAME")

        session_id = request.cookies.get(session_name)
        del UserSession.user_id_by_session_id(session_id)
