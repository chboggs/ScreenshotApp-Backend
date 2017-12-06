# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Entry point for the server application."""

from factory import app, db, image_dir
from http_codes import Status
from models import User, Image, Viewable, Comments

import traceback
import hashlib
import os, errno, hashlib
from datetime import datetime
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

import controllers

app.register_blueprint(controllers.api_image_blueprint)
app.register_blueprint(controllers.details_blueprint)
app.register_blueprint(controllers.login_blueprint)
app.register_blueprint(controllers.logout_blueprint)
app.register_blueprint(controllers.main_blueprint)
app.register_blueprint(controllers.new_user_blueprint)
app.register_blueprint(controllers.overview_blueprint)

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
    # db.drop_all()

if __name__ == '__main__':
    create_image_store()

    port = int(os.environ.get('$PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)
