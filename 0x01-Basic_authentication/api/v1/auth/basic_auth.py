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
