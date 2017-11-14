# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Entry point for the server application."""

from . import create_app

import json
import traceback
import hashlib
import os, errno, hashlib
from datetime import datetime
from flask import Flask, Response, request, jsonify, current_app, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, current_user , login_required
from gevent.wsgi import WSGIServer

from .http_codes import Status
from .models import db, User, Image, Viewable, Comments

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
    # db.drop_all()


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

    m = hashlib.new('sha512')
    m.update(password.encode('utf-8'))
    password = m.hexdigest()

    registered_user = User.query.filter(User.username == username, User.password == password).first()

    if not registered_user:
        return jsonify({"msg": "Invalid login"}), Status.HTTP_BAD_REQUEST

    login_user(registered_user)

    return jsonify({"msg": "Login successful"}), Status.HTTP_OK_BASIC

@app.route('/api/new-user', methods=['POST'])
def new_user():

    params = request.get_json()
    username = params.get('username', None)
    password = params.get('password', None)
    first_name = params.get('first_name', None)
    last_name = params.get('last_name', None)
    email = params.get('email', None)

    if not username or not password or not first_name or not last_name or not email:
        return jsonify({"msg": "Missing required parameter"}), Status.HTTP_BAD_REQUEST

    m = hashlib.new('sha512')
    m.update(password.encode('utf-8'))
    password = m.hexdigest()

    if User.query.filter(User.username == username).first() or User.query.filter(User.email == email).first():
        return jsonify({"msg": "Username or email taken"}), Status.HTTP_BAD_REQUEST

    db.session.add(User(
        username=username, email=email, password=password, first_name=first_name, last_name=last_name
        ))
    db.session.commit()

    return jsonify({"msg": "Successfully created user"}), Status.HTTP_OK_BASIC

@app.route('/api/new-image', methods=['POST'])
@login_required
def new_image():
    if 'image' not in request.files:
        return jsonify({"msg": "Missing image"}), Status.HTTP_BAD_REQUEST
    new_im = request.files['image']
    caption = ""
    if "caption" in request.form:
        caption = request.form["caption"]
    name = new_im.filename

    if not name or name == '' or len(name) > 50:
        return jsonify({"msg": "File must have a valid name"}), Status.HTTP_BAD_REQUEST

    path_to_image = os.path.join(image_dir, name)
    fw = open(path_to_image, 'wb')
    fw.write(new_im.read())
    fw.close()

    db.session.add(Image(
        name=name, owner=current_user.username, path_to_image=path_to_image, caption=caption
        ))
    db.session.commit()

    return jsonify({"msg": "Successfully added image"}), Status.HTTP_OK_BASIC

@app.route('/api/delete-image', methods=['DELETE'])
@login_required
def delete_image():

    params = request.get_json()
    image_name = params.get('image_name', None)

    if not image_name:
        return jsonify({"msg": "Must specify image name"}), Status.HTTP_BAD_REQUEST

    victim = Image.query.filter(Image.name == image_name).first()
    if not victim:
        return jsonify({"msg": "Image does not exist"}), Status.HTTP_BAD_REQUEST

    if current_user.username != victim.owner:
        return jsonify({"msg": "Current user does not own the specified image"}), Status.HTTP_BAD_UNAUTHORIZED

    comments = Comments.query.filter(Comments.parent_image == victim.name)
    for comment in comments:
        db.session.delete(comment)
        db.session.commit()

    db.session.delete(victim)
    db.session.commit()

    path_to_image = os.path.join(image_dir, image_name)
    if not os.path.exists(path_to_image):
        return jsonify({"msg": "Could not find image on server"}), Status.HTTP_SERVICE_UNAVAILABLE

    try:
        os.remove(path_to_image)
    except OSError as e:
        print(e)
        return jsonify({"msg": "OS error when deleting image"}), Status.HTTP_SERVICE_UNAVAILABLE

    if Image.query.filter(Image.name == image_name).first():
        return jsonify({"msg": "Unsuccessful delete"}), Status.HTTP_SERVICE_UNAVAILABLE

    return jsonify({"msg": "Successfully deleted image"}), Status.HTTP_OK_BASIC


@app.route('/api/add-viewer', methods=['POST'])
@login_required
def add_viewer():
    params = request.get_json()
    filename = params.get('filename', None)
    new_viewer = params.get('new-viewer', None)

    if not filename or not new_viewer:
        return jsonify({"msg": "Missing required parameter"}), Status.HTTP_BAD_REQUEST

    if not User.query.filter(User.username == new_viewer).first() or not Image.query.filter(Image.name == filename).first():
        return jsonify({"msg": "Invalid user or filename"}), Status.HTTP_BAD_REQUEST

    owner = User.query.filter(User.username == Image.query.filter(Image.name == filename).first().owner).first()

    if new_viewer == owner.username:
        return jsonify({"msg": "Is owner"}), Status.HTTP_BAD_REQUEST
    if Viewable.query.filter(Viewable.image_name == filename and Viewable.user_name == new_viewer).first():
        return jsonify({"msg": "Can already view"}), Status.HTTP_BAD_REQUEST

    db.session.add(Viewable(
        image_name=filename, user_name=new_viewer
        ))
    db.session.commit()


    return jsonify({"msg": "Successfully added viewer"}), Status.HTTP_OK_BASIC


@app.route('/api/delete-viewer', methods=['DELETE'])
@login_required
def delete_viewer():
    params = request.get_json()
    filename = params.get('filename', None)
    victim = params.get('victim', None)

    if not filename or not victim:
        return jsonify({"msg": "Missing required parameter"}), Status.HTTP_BAD_REQUEST

    if not User.query.filter(User.username == victim).first() or not Image.query.filter(Image.name == filename).first():
        return jsonify({"msg": "Invalid user or filename"}), Status.HTTP_BAD_REQUEST

    owner = User.query.filter(User.username == Image.query.filter(Image.name == filename).first().owner).first()

    if victim == owner.username:
        return jsonify({"msg": "Cannot delete owner"}), Status.HTTP_BAD_REQUEST
    if not Viewable.query.filter(Viewable.image_name == filename and Viewable.user_name == victim).first():
        return jsonify({"msg": "User cannot view already"}), Status.HTTP_BAD_REQUEST

    db.session.delete(Viewable.query.filter(Viewable.image_name == filename and Viewable.user_name == victim).first())
    db.session.commit()


    return jsonify({"msg": "Successfully deleted viewer"}), Status.HTTP_OK_BASIC


@app.route('/api/get-image', methods=['GET'])
@login_required
def get_image():
    filename = request.args.get('filename')

    if not filename:
        return jsonify({"msg": "Missing required parameter"}), Status.HTTP_BAD_REQUEST
    if not Image.query.filter(Image.name == filename).first():
        return jsonify({"msg": "Invalid filename"}), Status.HTTP_BAD_REQUEST

    if not Image.query.filter(Image.name == filename).first().owner == current_user.username and not Viewable.query.filter(Viewable.image_name == filename and Viewable.user_name == current_user.username).first():
        return jsonify({"msg": "Cannot view image"}), Status.HTTP_BAD_UNAUTHORIZED

    # Okay they can view the image

    return send_file(os.path.join(image_dir, filename), mimetype='image/gif'), Status.HTTP_OK_BASIC

@app.route('/api/get-owned-images', methods=['GET'])
@login_required
def get_owned_images():

    if not Image.query.filter(Image.owner == current_user.username).first():
        return jsonify({"msg": "Current user owns no images"}), Status.HTTP_BAD_REQUEST

    owned_images = Image.query.filter(Image.owner == current_user.username)

    image_info = []
    image_names = []
    captions = []
    for image in owned_images:
        image_names.append(image.name)
        captions.append(image.caption)

    image_info = [{"name": name, "caption": caption} for name,caption in zip(image_names, captions) ]
    return jsonify({"images": image_info})


@app.route('/api/get-viewable-images', methods=['GET'])
@login_required
def get_viewable_images():

    if not Viewable.query.filter(Viewable.user_name == current_user.username).first():
        return jsonify({"msg": "Current user cannot view anyone else's images"}), Status.HTTP_BAD_REQUEST

    viewable_filenames = Viewable.query.filter(Viewable.user_name == current_user.username)
    viewable_images = []
    for viewable in viewable_filenames:
        image = Image.query.filter(Image.name == viewable.image_name).first()
        viewable_images.append(image)

    image_info = []
    image_names = []
    captions = []
    owners = []
    for image in viewable_images:
        image_names.append(image.name)
        captions.append(image.caption)
        owners.append(image.owner)

    image_info = [{"name": name, "caption": caption, "owner": owner} for name,caption,owner in zip(image_names, captions, owners) ]
    return jsonify({"images": image_info})


@app.route('/api/edit-caption', methods=['POST'])
@login_required
def edit_caption():
    params = request.get_json()
    filename = params.get('filename', None)
    new_caption = params.get('new-caption', None)

    if not filename or not new_caption:
        return jsonify({"msg": "Missing required parameter"}), Status.HTTP_BAD_REQUEST
    if not Image.query.filter(Image.name == filename).first():
        return jsonify({"msg": "Invalid filename"}), Status.HTTP_BAD_REQUEST

    if not Image.query.filter(Image.name == filename).first().owner == current_user.username:
        return jsonify({"msg": "You do not own this image"}), Status.HTTP_BAD_UNAUTHORIZED

    # Okay they can edit the caption
    Image.query.filter(Image.name == filename).first().caption = new_caption

    return jsonify({"msg": "Successfully edited caption"}), Status.HTTP_OK_BASIC

@app.route('/api/add-comment', methods=['POST'])
@login_required
def add_comment():
    params = request.get_json()
    filename = params.get('filename', None)
    comment = params.get('comment', None)

    if not filename or not comment:
        return jsonify({"msg": "Missing required parameter"}), Status.HTTP_BAD_REQUEST
    if not Image.query.filter(Image.name == filename).first():
        return jsonify({"msg": "Invalid filename"}), Status.HTTP_BAD_REQUEST

    if not Image.query.filter(Image.name == filename).first().owner == current_user.username and not Viewable.query.filter(Viewable.image_name == filename and Viewable.user_name == current_user.username).first():
        return jsonify({"msg": "You do not have permissions for this image"}), Status.HTTP_BAD_UNAUTHORIZED

    # Now can comment
    db.session.add(Comments(
        parent_image=filename, author=current_user.username, comment_string=comment
        ))
    db.session.commit()

    return jsonify({"msg": "Successfully added comment"}), Status.HTTP_OK_BASIC

@app.route('/api/get-comments', methods=['GET'])
@login_required
def get_comments():
    filename = request.args.get('filename')

    if not filename:
        return jsonify({"msg": "Missing required parameter"}), Status.HTTP_BAD_REQUEST
    if not Image.query.filter(Image.name == filename).first():
        return jsonify({"msg": "Invalid filename"}), Status.HTTP_BAD_REQUEST

    if not Image.query.filter(Image.name == filename).first().owner == current_user.username and not Viewable.query.filter(Viewable.image_name == filename and Viewable.user_name == current_user.username).first():
        return jsonify({"msg": "You do not have permissions for this image"}), Status.HTTP_BAD_UNAUTHORIZED

    image_comments = Comments.query.filter(Comments.parent_image == filename).order_by(Comments.timestamp)

    authors = []
    comment_strings = []
    for comment in image_comments:
        authors.append(comment.author)
        comment_strings.append(comment.comment_string)

    comments = [{"Author": aut, "Comment": comm} for aut,comm in zip(authors, comment_strings) ]

    return jsonify({"comments": comments})


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
