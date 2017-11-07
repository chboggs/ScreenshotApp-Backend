# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Entry point for the server application."""

from . import create_app

import json
import traceback
import hashlib
from datetime import datetime
from flask import Flask, Response, request, jsonify, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from gevent.wsgi import WSGIServer

from .http_codes import Status
from .models import db, User

app = create_app()

login_manager = LoginManager()
login_manager.init_app(app)


@app.before_first_request
def init():
    """Initialize the application with defaults."""
    db.create_all()



# @app.route("/api/logout", methods=['POST'])
# def logout():
#     """Logout the currently logged in user."""
#     # TODO: handle this logout properly, very weird implementation.
#     identity = get_jwt_identity()
#     if not identity:
#         return jsonify({"msg": "Token invalid"}), Status.HTTP_BAD_UNAUTHORIZED
#     return 'logged out successfully', Status.HTTP_OK_BASIC


# @app.route('/api/login', methods=['POST'])
# def login():
#     """View function for login view."""

#     params = request.get_json()
#     username = params.get('username', None)
#     password = params.get('password', None)

#     if not username:
#         return jsonify({"msg": "Missing username parameter"}), Status.HTTP_BAD_REQUEST
#     if not password:
#         return jsonify({"msg": "Missing password parameter"}), Status.HTTP_BAD_REQUEST

#     # TODO Check from DB here
#     if username != 'admin' or password != 'admin':
#         return jsonify({"msg": "Bad username or password"}), Status.HTTP_BAD_UNAUTHORIZED

#     # Identity can be any data that is json serializable
#     # TODO: rather than passing expiry time here explicitly, decode token on client side. But I'm lazy.
#     ret = {'jwt': create_jwt(identity=username), 'exp': datetime.utcnow() + current_app.config['JWT_EXPIRES']}
#     return jsonify(ret), 200

@app.route('/api/new-image', methods=['POST'])
def new_user():
    params = request.get_json()
    username = params.get('username', None)
    hashed_password = params.get('password', None)
    first_name = params.get('first_name', None)
    last_name = params.get('last_name', None)
    email = params.get('email', None)

    if not username or not hashed_password or not first_name or not last_name or not email:
        return jsonify({"msg": "Missing required parameter"}), Status.HTTP_BAD_REQUEST

    if User.query.filter(User.username == username).first() or User.query.filter(User.email == email).first():
        return jsonify({"msg": "Username or email taken"}), Status.HTTP_BAD_REQUEST
    
    db.session.add(User(
        username=username, email=email, password=hashed_password, first_name=first_name, last_name=last_name
        ))
    db.session.commit()

    return jsonify({"msg": "Successfully created user"}), Status.HTTP_OK_BASIC

# @app.route('/api/new-image', methods=['POST'])
# def new_image():

# @app.route('/api/new-user', methods=['GET'])
# def get_image_ids():


def main():
    """Main entry point of the app."""
    try:
        port = 8080
        ip = '0.0.0.0'
        http_server = WSGIServer((ip, port),
                                 app)
        print("Server started at: {0}:{1}".format(ip, port))
        http_server.serve_forever()
    except Exception as exc:
        print("Error")
        print(exc)
    finally:
        # Do something here
        pass
