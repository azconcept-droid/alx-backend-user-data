#!/usr/bin/env python3
"""
Route module for the API
"""
from flask import Flask, jsonify, request, url_for
from flask import abort, make_response, redirect
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/")
def index():
    """Home page route"""
    return jsonify({"message": "Bienvenue"})


@app.route("/profile")
def profile():
    """Profile page route"""
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200

    abort(403)


@app.route("/users", methods=['POST'])
def users() -> str:
    """ register new user
    POST /api/v1/users
    JSON body:
      - email
      - password
    Return:
      - User object JSON represented
      - 400 if can't create the new User
    """
    try:
        email = request.form.get('email')
        password = request.form.get('password')
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=['POST'])
def login() -> str:
    """ login user session
    POST /api/v1/sessions
    JSON body:
      - email
      - password
    Return:
      - response object JSON represented
      - 400 if can't create the new User
    """

    email = request.form.get('email')
    password = request.form.get('password')
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie('session_id', session_id)
        return response

    abort(401)


@app.route("/sessions", methods=['DELETE'])
def logout() -> str:
    """ logout route
    DELETE /api/v1/sessions
    Return:
      - redirect to GET /
      - 403 if user does not exist
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect(url_for('index'))
    else:
        abort(403)


@app.route("/reset_password", methods=['POST'])
def get_reset_password_token():
    """ request for password reset
    POST /api/v1/reset_password
    JSON body:
      - email
    Return:
      - reset_token
      - 403 if email not found
    """
    email = request.form.get('email')
    try:
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": token}), 200
    except ValueError:
        abort(403)


@app.route("/update_password", methods=['PUT'])
def update_password():
    """ update password
    PUT /api/v1/update_password
    JSON body:
      - email
      - reset_token
      - new_password
    Return:
      - 200 update password
      - 403 invalid token
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')

    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
