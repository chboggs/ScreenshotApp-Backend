from flask import *
from ..models import Image
from ..factory import db
from ..http_codes import *
from ..app import image_dir

api_image = Blueprint('api_image', __name__, template_folder='templates')

@api_image.route('/api/new-image', methods=['POST'])
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

    current_user = session['username']

    db.session.add(Image(
        name=name, owner=current_user.username, path_to_image=path_to_image, caption=caption
        ))
    db.session.commit()

    return jsonify({"msg": "Successfully added image"}), Status.HTTP_OK_BASIC

@api_image.route('/api/new-image-hololens', methods=['POST'])
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

    path_to_image = os.path.join(image_dir, name)
    fw = open(path_to_image, 'wb')
    fw.write(new_im.read())
    fw.close()

    db.session.add(Image(
        name=name, owner=username, path_to_image=path_to_image, caption=caption
        ))
    db.session.commit()

    return jsonify({"msg": "Successfully added image"}), Status.HTTP_OK_BASIC
