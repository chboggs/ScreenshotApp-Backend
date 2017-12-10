import os, sys, inspect, json, hashlib
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from flask import *
from models import Image, Comments, User
from factory import db
from http_codes import *
from factory import image_dir

api_image_blueprint = Blueprint('api_image_blueprint', __name__, template_folder='templates')

def find_new_name(name):
    index = len(name)
    for i in range(len(name) - 1, -1, -1):
        if name[i] == '.':
            index = i
            break

    if index == len(name):
        return name

    first_half = name[:index] + '('
    second_half = ')' + name[index:]

    counter = 1
    success = False
    new_name = ""

    while not success:
        new_name = first_half + str(counter) + second_half
        if not Image.query.filter(Image.name == new_name).first():
            success = True
        else:
            counter = counter + 1

    return new_name

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

    if Image.query.filter(Image.name == name).first():
        new_name = find_new_name(name)
        if new_name == name:
            return jsonify({"msg": "Filename already exists, and server is unable to find a new name"}), 500
        else:
            name = new_name

    m = hashlib.new('sha512')
    m.update(password.encode('utf-8'))
    password = m.hexdigest()
    registered_user = User.query.filter(User.username == username, User.password == password).first()
    if not registered_user:
        return jsonify({"msg": "Invalid login"}), Status.HTTP_BAD_REQUEST

    if not name or name == '' or len(name) > 50:
        return jsonify({"msg": "File must have a valid name"}), Status.HTTP_BAD_REQUEST

    path_to_image = os.path.join(image_dir, name)
    fw = open(path_to_image, 'wb')
    fw.write(new_im.read())
    fw.close()

    db.session.add(Image(
        name=name, owner=username, path_to_image=path_to_image, caption=caption
        ))
    db.session.commit()

    added_image = Image.query.filter(Image.name == name).first()
    if not added_image:
        return jsonify({"msg": "Error adding image to server"}), 500

    return jsonify({ "msg": "Successfully added image",
                     "url": "https://screenshot-tool-eecs498.herokuapp.com/details?image_id=" + str(added_image.id)
                   }), Status.HTTP_OK_BASIC

@api_image_blueprint.route('/api/get-image', methods=['GET'])
def get_image():
    if 'username' not in session:
        return jsonify({"msg": "Must be authenticated"}), Status.HTTP_BAD_FORBIDDEN

    username = session['username']
    user = User.query.filter(User.username == username).first()

    if not user:
        return jsonify({"msg": "Must be authenticated"}), Status.HTTP_BAD_FORBIDDEN

    id = request.args.get('id')

    if not id:
        return jsonify({"msg": "Missing required parameter"}), Status.HTTP_BAD_REQUEST

    image = Image.query.filter(Image.id == id).first()

    if not image:
        return jsonify({"msg": "Invalid image id"}), Status.HTTP_BAD_REQUEST

    if not image.owner == username and not Viewable.query.filter(Viewable.image_id == id and Viewable.user_name == username).first():
        return jsonify({"msg": "Cannot view image"}), Status.HTTP_BAD_UNAUTHORIZED

    # Okay they can view the image

    return send_file(os.path.join(image_dir, image.name), mimetype='image/gif'), Status.HTTP_OK_BASIC
