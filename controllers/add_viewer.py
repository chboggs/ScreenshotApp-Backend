import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from flask import *
from models import User
from factory import db
from http_codes import *

add_viewer_blueprint = Blueprint('add_viewer_blueprint', __name__, template_folder='templates')

@add_viewer_blueprint.route('/add-viewer', methods=['POST'])
def add_viewer():
    params = request.get_json()
    image_id = params.get('image_id', None)
    new_viewer = params.get('new_viewer', None)

    if not image_id or not new_viewer:
        return jsonify({"msg": "Missing required parameter"}), Status.HTTP_BAD_REQUEST

    if not User.query.filter(User.username == new_viewer).first() or not Image.query.filter(Image.id == image_id).first():
        return jsonify({"msg": "Invalid user or filename"}), Status.HTTP_BAD_REQUEST

    owner = User.query.filter(User.username == Image.query.filter(Image.id == image_id).first().owner).first()
    image = Image.query.filter(Image.id == image_id).first()

    results = Viewable.query.filter(Viewable.image_name == image.name)
    for result in results:
        print(result)

    print("result:")
    print(Viewable.query.filter(Viewable.image_name == image.name and Viewable.user_name == new_viewer).first())
    print("image name: " + image.name + " user name: " + new_viewer)

    if new_viewer == owner.username:
        return jsonify({"msg": "Is owner"}), Status.HTTP_BAD_REQUEST
    if Viewable.query.filter(Viewable.image_name == image.name and Viewable.user_name == new_viewer).first():
        return jsonify({"msg": "Can already view"}), Status.HTTP_BAD_REQUEST

    db.session.add(Viewable(
        image_name=image.name, image_id=image_id, user_name=new_viewer
        ))
    db.session.commit()

    return jsonify({"msg": "Successfully added viewer"}), Status.HTTP_OK_BASIC
