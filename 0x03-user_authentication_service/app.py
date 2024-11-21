#!/usr/bin/env python3
"""
Route module for the API
"""
from flask import Flask, jsonify, request, abort, make_response
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/")
def index():
    """Home page route"""
    return jsonify({"message": "Bienvenue"})


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
      - User object JSON represented
      - 400 if can't create the new User
    """

    email = request.form.get('email')
    password = request.form.get('password')
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        response = make_response("Cookie set using headers!")
        value = 'session_id={}; Path=/'.format(session_id)
        response.headers['Set-Cookie'] = value
        return jsonify({"email": email, "message": "logged in"})

    abort(401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
