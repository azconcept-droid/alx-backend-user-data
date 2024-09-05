#!/usr/bin/env python3
""" Module of Session Auth views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def create_user_login_session() -> str:
    """ POST /api/v1/auth_session/login
    JSON body:
      - email
      - password
    Return:
      - User login session
      - 400 if can't login user
    """
    error_msg = None
    user_email = request.form.get('email')
    user_passwrd = request.form.get('password')

    if user_email is None:
        error_msg = "email missing"
        return jsonify({'error': error_msg}), 400

    if user_passwrd is None:
        error_msg = "password missing"
        return jsonify({'error': error_msg}), 400

    try:
        users = User.search({'email': user_email})
    except Exception:
        error_msg = "no user found for this email"
        return jsonify({'error': error_msg}), 404

    for user in users:
        is_pwd = user.is_valid_password(user_passwrd)
        if is_pwd:
            from api.v1.app import auth
            session_id = auth.create_session(user.id)
            res = jsonify(user.to_json())
            res.set_cookie(getenv('SESSION_NAME'), session_id)
            return res, 200
        else:
            error_msg = "wrong password"
            return jsonify({'error': error_msg}), 401


@app_views.route('/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def cancel_user_login_session() -> str:
    """ DELETE /api/v1/auth_session/logout
    JSON body:
      - email
    Return:
      - User LOGOUT session
      - 404 if can't logout user
    """
    from api.v1.app import auth
    user_logout = auth.destroy_session(request)
    if user_logout:
        return jsonify({}), 200
    else:
        abort(404)
