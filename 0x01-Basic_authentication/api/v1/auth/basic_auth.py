#!/usr/bin/env python3
""" Basic Authentication module
"""
from api.v1.auth.auth import Auth
from flask import request


class BasicAuth(Auth):
    """ Basic auth class """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ extract base64 code """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        # If auth header don't have "Basic "
        if authorization_header[:6] != 'Basic ':
            return None
        # extract base64 token
        base64_token = authorization_header.split(' ')[1]

        return base64_token
