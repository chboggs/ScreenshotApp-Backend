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
    if 'username' not in session:
        return "Must be authenticated", Status.HTTP_BAD_FORBIDDEN

    current_user = session['username']

    image_id = request.form['image_id']
    new_viewer = request.form['new_viewer']

    if not image_id or not new_viewer:
        return "Missing required parameter", Status.HTTP_BAD_REQUEST

    if not User.query.filter(User.username == new_viewer).first() or not Image.query.filter(Image.id == image_id).first():
        return "Invalid user or filename", Status.HTTP_BAD_REQUEST

    owner = User.query.filter(User.username == Image.query.filter(Image.id == image_id).first().owner).first()
    if current_user != owner.username:
        return "You do not own this image", Status.HTTP_BAD_FORBIDDEN

    image = Image.query.filter(Image.id == image_id).first()

    if new_viewer == owner.username:
        return "User " + new_viewer + " owns this image", Status.HTTP_BAD_REQUEST

    viewables = Viewable.query.all()
    for viewable in viewables:
        if viewable.image_id == image.id and viewable.user_name == new_viewer:
            return "User " + new_viewer + " can already view this image", Status.HTTP_BAD_REQUEST

    db.session.add(Viewable(
        image_name=image.name, image_id=image_id, user_name=new_viewer
        ))
    db.session.commit()

    return "Successfully granted permission to " + new_viewer, Status.HTTP_OK_BASIC

@api_details_blueprint.route('/api/add_comment', methods=['POST'])
def add_comment_api():
    if 'username' not in session:
        return "Must be authenticated", Status.HTTP_BAD_FORBIDDEN

    current_user = session['username']

    image_id = request.form['image_id']
    comment = request.form['comment']

    if not image_id or not comment:
        return "Missing required parameter", Status.HTTP_BAD_REQUEST
    if not Image.query.filter(Image.id == image_id).first():
        return "Invalid image id", Status.HTTP_BAD_REQUEST

    if not Image.query.filter(Image.id == image_id).first().owner == session['username'] and not Viewable.query.filter(Viewable.image_id == image_id and Viewable.user_name == current_user).first():
        return "You do not have permissions for this image", Status.HTTP_BAD_UNAUTHORIZED

    # Now can comment
    db.session.add(Comments(
        parent_image=image_id, author=current_user, comment_string=comment
        ))
    db.session.commit()

    return "Successfully added comment", Status.HTTP_OK_BASIC
