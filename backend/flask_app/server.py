# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Entry point for the server application."""

from . import create_app

import json
import traceback
import hashlib
import os, errno
from datetime import datetime
from flask import Flask, Response, request, jsonify, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, current_user , login_required
from gevent.wsgi import WSGIServer

from .http_codes import Status
from .models import db, User

app = create_app()

login_manager = LoginManager()
login_manager.init_app(app)

cur_dir = os.getcwd()
image_dir = os.path.join(cur_dir, 'images')

def create_image_store():
    try:
        if not os.path.exists(image_dir):
            os.makedirs(image_dir)
    except OSError as e:
        print(e)
        create_image_store()

@app.before_first_request
def init():
    """Initialize the application with defaults."""
    db.create_all()


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/api/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"msg": "Logout successful"}), Status.HTTP_OK_BASIC


@app.route('/api/login', methods=['POST'])
def login():

    params = request.get_json()
    username = params.get('username', None)
    password = params.get('password', None)

    if not username or not password:
        return jsonify({"msg": "Missing login parameter"}), Status.HTTP_BAD_REQUEST

    registered_user = User.query.filter(User.username == username, User.password == password).first()

    if not registered_user:
        return jsonify({"msg": "Invalid login"}), Status.HTTP_BAD_REQUEST

    login_user(registered_user)

    return jsonify({"msg": "Login successful"}), Status.HTTP_OK_BASIC

@app.route('/api/new-user', methods=['POST'])
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

# @app.route('/api/get-image', methods=['GET'])
# def new_image():


def main():
    """Main entry point of the app."""
    try:
        port = 8080
        ip = '0.0.0.0'
        create_image_store()
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
