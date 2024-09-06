#!/usr/bin/env python3
""" User session module
"""
from models.base import Base
import uuid


class UserSession(Base):
    """ User session class """

    def __init__(self, *args: list, **kwargs: dict):
        """ initialize a user session instance """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('id')
        self.session_id = kwargs.get('session_id', str(uuid.uuid4()))