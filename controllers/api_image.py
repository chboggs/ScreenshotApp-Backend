import os, sys, inspect, json, hashlib
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from flask import *
from models import Image, Comments, User
from factory import db
from http_codes import *
from factory import relative_image_dir

api_image_blueprint = Blueprint('api_image_blueprint', __name__, template_folder='templates')

@api_image_blueprint.route('/api/new-image-hololens', methods=['POST'])
def new_image_hololens():
    username = request.form['username']
    password = request.form['password']

    if not username or not password:
        return jsonify({"msg": "Missing login parameter"}), Status.HTTP_BAD_REQUEST
    if 'image' not in request.files:
        return jsonify({"msg": "Missing image"}), Status.HTTP_BAD_REQUEST
    new_im = request.files['image']
    caption = ""
    if "caption" in request.form:
        caption = request.form["caption"]
    name = new_im.filename

    m = hashlib.new('sha512')
    m.update(password.encode('utf-8'))
    password = m.hexdigest()
    registered_user = User.query.filter(User.username == username, User.password == password).first()
    if not registered_user:
        return jsonify({"msg": "Invalid login"}), Status.HTTP_BAD_REQUEST

    if not name or name == '' or len(name) > 50:
        return jsonify({"msg": "File must have a valid name"}), Status.HTTP_BAD_REQUEST

    path_to_image = relative_image_dir + '/' + name
    fw = open(path_to_image, 'wb')
    fw.write(new_im.read())
    fw.close()

    db.session.add(Image(
        name=name, owner=username, path_to_image=path_to_image, caption=caption
        ))
    db.session.commit()

    return jsonify({"msg": "Successfully added image"}), Status.HTTP_OK_BASIC
