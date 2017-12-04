import os, sys, inspect, json
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from flask import *
from models import Image, Comments
from factory import db
from http_codes import *
from factory import image_dir

api_image_blueprint = Blueprint('api_image_blueprint', __name__, template_folder='templates')

@api_image_blueprint.route('/api/new-image', methods=['POST'])
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

    path_to_image = os.path.join(image_dir, name)
    fw = open(path_to_image, 'wb')
    fw.write(new_im.read())
    fw.close()

    db.session.add(Image(
        name=name, owner=username, path_to_image=path_to_image, caption=caption
        ))
    db.session.commit()

    return jsonify({"msg": "Successfully added image"}), Status.HTTP_OK_BASIC

@api_image_blueprint.route('/api/delete-image', methods=['DELETE'])
def delete_image():

    params = request.get_json()
    image_name = params.get('image_name', None)

    if not image_name:
        return jsonify({"msg": "Must specify image name"}), Status.HTTP_BAD_REQUEST

    victim = Image.query.filter(Image.name == image_name).first()
    if not victim:
        return jsonify({"msg": "Image does not exist"}), Status.HTTP_BAD_REQUEST

    if session['username'] != victim.owner:
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

@api_image_blueprint.route('/api/get-image', methods=['GET'])
def get_image():
    id = request.args.get('id')

    if not id:
        return jsonify({"msg": "Missing required parameter"}), Status.HTTP_BAD_REQUEST

    image = Image.query.filter(Image.id == id).first()

    if not image:
        return jsonify({"msg": "Invalid image id"}), Status.HTTP_BAD_REQUEST

    if not image.owner == current_user.username and not Viewable.query.filter(Viewable.image_id == id and Viewable.user_name == current_user.username).first():
        return jsonify({"msg": "Cannot view image"}), Status.HTTP_BAD_UNAUTHORIZED

    # Okay they can view the image

    return send_file(os.path.join(image_dir, image.name), mimetype='image/gif'), Status.HTTP_OK_BASIC

@api_image_blueprint.route('/api/get-owned-images', methods=['GET'])
def get_owned_images():

    if not Image.query.filter(Image.owner == current_user.username).first():
        return jsonify({"msg": "Current user owns no images"}), Status.HTTP_BAD_REQUEST

    owned_images = Image.query.filter(Image.owner == current_user.username)

    image_info = []
    image_names = []
    image_ids = []
    captions = []
    for image in owned_images:
        image_names.append(image.name)
        image_ids.append(image.id)
        captions.append(image.caption)

    image_info = [{"name": name, "id": id, "caption": caption} for name,id,caption in zip(image_names, image_ids, captions) ]
    return jsonify({"images": image_info})

@api_image_blueprint.route('/api/get-viewable-images', methods=['GET'])
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
    image_ids = []
    captions = []
    owners = []
    for image in viewable_images:
        image_names.append(image.name)
        image_ids.append(image.id)
        captions.append(image.caption)
        owners.append(image.owner)

    image_info = [{"name": name, "id": id, "caption": caption, "owner": owner} for name,id,caption,owner in zip(image_names, image_ids, captions, owners) ]
    return jsonify({"images": image_info})
