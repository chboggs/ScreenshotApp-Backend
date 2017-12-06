import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from flask import *
from models import User, Image, Comments, Viewable
from factory import db
from http_codes import *

details_blueprint = Blueprint('details_blueprint', __name__, template_folder='templates')

@details_blueprint.route('/details', methods=['GET'])
def image_details():
    if 'username' not in session:
        return redirect(url_for('login_blueprint.login_user'))

    username = session['username']
    user = User.query.filter(User.username == username).first()

    if not user:
        return redirect(url_for('login_blueprint.login_user'))

    query_params = dict(request.args)
    if 'image_id' not in query_params:
        options = {
            'user': user,
            'message': 'Image not found'
        }
        return render_template('error.html', **options), Status.HTTP_BAD_NOTFOUND

    image_id = query_params['image_id'][0]
    image = Image.query.filter(Image.id == image_id).first()

    owner = True

    if image.owner != username:
        owner = False

        if not Viewable.query.filter(Viewable.image_name == image.name and Viewable.user_name == username).first():
            options = {
                'user': user,
                'message': 'You do not own this image or have permission to view it'
            }
            return render_template('error.html', **options), Status.HTTP_BAD_FORBIDDEN

    comments = Comments.query.filter(Comments.parent_image == image.name).all()

    options = {
        'user': user,
        'image': image,
        'comments': comments,
        'owner': owner,
        'add_viewer_message': ""
    }
    return render_template('details.html', **options), Status.HTTP_OK_BASIC
