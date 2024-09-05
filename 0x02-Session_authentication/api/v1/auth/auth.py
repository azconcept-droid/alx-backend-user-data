#!/usr/bin/env python3
""" Authentication module
"""
from flask import request
from typing import List, TypeVar
from os import getenv


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
            # allow wildcard /*
            if route[-1] == '*':
                wild_route = route[:len(route) - 1]
                if wild_route == path[:len(route) - 1]:
                    return False
            # append / to route
            if route[-1] != '/':
                route = route + '/'
            if route == path:
                return False

        return True

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

    def session_cookie(self, request=None):
        """ return cookie value from a request """
        if request is None:
            None
        session_name = getenv("SESSION_NAME")

        return request.cookies.get(session_name)
