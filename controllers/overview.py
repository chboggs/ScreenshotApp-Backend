import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from flask import *
from models import User, Image, Viewable
from factory import db
from http_codes import *

overview_blueprint = Blueprint('overview_blueprint', __name__, template_folder='templates')

@overview_blueprint.route('/overview', methods=['GET'])
def user_overview():
    if 'username' not in session:
        return redirect(url_for('login_blueprint.login_user'))

    username = session['username']
    user = User.query.filter(User.username == username).first()

    if not user:
        return redirect(url_for('login_blueprint.login_user'))

    owned_images = Image.query.filter(Image.owner == username).all()
    viewables = Viewable.query.filter(Viewable.user_name == username).all()
    viewable_images = []

    for viewable in viewables:
        viewable_images.append(Image.query.filter(Image.name == viewable.image_name).first())

    options = {
        "owned": len(owned_images) != 0,
        "owned_images": owned_images,
        "viewable": len(viewable_images) != 0,
        "viewable_images": viewable_images,
        "user": user
    }

    return render_template('overview.html', **options), Status.HTTP_OK_BASIC
