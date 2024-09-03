#!/usr/bin/env python3
""" Authentication module
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """ Authentication class """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Method that determine route that is authorized
        """
        if path is None:
            return True
        # append / to path
        if path[-1] != '/':
            path = path + '/'

        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        for route in excluded_paths:
            if route == path:
                return True

        return False

    def authorization_header(self, request=None) -> str:
        """ Check client request header"""
        if request is None:
            return None

        auth_header = request.headers.get('Authorization')

        if auth_header is None:
            return None

        return auth_header

    def current_user(self, request=None) -> TypeVar('User'):
        """ Authenticated user """
        return None
