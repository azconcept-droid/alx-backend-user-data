#!/usr/bin/env python3
""" Basic Authentication module
"""
from api.v1.auth.auth import Auth
from flask import request
from typing import TypeVar
import base64
from models.user import User


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

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """ decode base64 auth token """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            encode_base64 = base64_authorization_header.encode("utf-8")
            decoded_base64 = base64.b64decode(encode_base64).decode("utf-8")
            return decoded_base64
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """ Extract user credentials """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ":" not in decoded_base64_authorization_header:
            return (None, None)
        user_info = decoded_base64_authorization_header.partition(':')

        return (user_info[0], user_info[2])

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """ Return user instance """
        if user_email is None or user_pwd is None:
            return None
        if not isinstance(user_pwd, str):
            return None
        if not isinstance(user_email, str):
            return None
        try:
            users = User.search({'email': user_email})
        except Exception:
            return None

        for user in users:
            is_passwrd = user.is_valid_password(user_pwd)
            if is_passwrd:
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """overloads Auth and retrieves
        the User instance for a request
        """
        basic_auth_header = self.authorization_header(request)
        if basic_auth_header is None:
            return None
        token = self.extract_base64_authorization_header(basic_auth_header)
        if token is None:
            return None
        decoded_token = self.decode_base64_authorization_header(token)
        if decoded_token is None:
            return None
        (user_name, user_pwd) = self.extract_user_credentials(decoded_token)
        if user_name is None or user_pwd is None:
            return None
        user_instance = self.user_object_from_credentials(user_name, user_pwd)
        if user_instance is None:
            return None
        return user_instance
