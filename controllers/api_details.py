import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from flask import *
from models import User, Image, Comments, Viewable
from factory import db
from http_codes import *

api_details_blueprint = Blueprint('api_details_blueprint', __name__, template_folder='templates')

@api_details_blueprint.route('/api/add_viewer', methods=['POST'])
def add_viewer_api():
    print("request")
    params = request.get_json()
    print(params)
    image_id = params.get('image_id', None)
    new_viewer = params.get('new_viewer', None)

    query_params = dict(request.args)

    if not image_id or not new_viewer:
        return "Missing required parameter", Status.HTTP_BAD_REQUEST

    if not User.query.filter(User.username == new_viewer).first() or not Image.query.filter(Image.id == image_id).first():
        return "Invalid user or filename", Status.HTTP_BAD_REQUEST

    owner = User.query.filter(User.username == Image.query.filter(Image.id == image_id).first().owner).first()
    current_user = session['username']
    if current_user != owner.username:
        return "You do not own this image", Status.HTTP_BAD_FORBIDDEN

    image = Image.query.filter(Image.id == image_id).first()

    if new_viewer == owner.username:
        return "User " + new_viewer + " owns this image", Status.HTTP_BAD_REQUEST
    if Viewable.query.filter(Viewable.image_name == image.name and Viewable.user_name == new_viewer).first():
        return "User " + new_viewer + " can already view this image", Status.HTTP_BAD_REQUEST

    db.session.add(Viewable(
        image_name=image.name, image_id=image_id, user_name=new_viewer
        ))
    db.session.commit()

    return "Successfully granted permission to " + new_viewer, Status.HTTP_OK_BASIC

@api_details_blueprint.route('/api/add_comment', methods=['POST'])
def add_comment_api():
    query_params = dict(request.args)

    if 'image_id' not in query_params or 'new_viewer' not in query_params:
        return "Missing required parameter", Status.HTTP_BAD_REQUEST

    image_id = query_params['image_id'][0]
    new_viewer = query_params['new_viewer'][0]

    if not User.query.filter(User.username == new_viewer).first() or not Image.query.filter(Image.id == image_id).first():
        return "Invalid user or filename", Status.HTTP_BAD_REQUEST

    owner = User.query.filter(User.username == Image.query.filter(Image.id == image_id).first().owner).first()
    current_user = session['username']
    if current_user != owner.username:
        return "You do not own this image", Status.HTTP_BAD_FORBIDDEN

    image = Image.query.filter(Image.id == image_id).first()

    if new_viewer == owner.username:
        return "User " + new_viewer + " owns this image", Status.HTTP_BAD_REQUEST
    if Viewable.query.filter(Viewable.image_name == image.name and Viewable.user_name == new_viewer).first():
        return "User " + new_viewer + " can already view this image", Status.HTTP_BAD_REQUEST

    db.session.add(Viewable(
        image_name=image.name, image_id=image_id, user_name=new_viewer
        ))
    db.session.commit()

    return "Successfully granted permission to " + new_viewer, Status.HTTP_OK_BASIC
