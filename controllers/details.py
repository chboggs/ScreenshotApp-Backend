import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from flask import *
from models import User, Image, Comments, Viewable
from factory import db
from http_codes import *

details_blueprint = Blueprint('details_blueprint', __name__, template_folder='templates')

def add_viewer(request, user, image):
    if image.owner != user.username:
        options = {
            'user': user,
            'message': 'You do not own this image'
        }
        return render_template('error.html', **options), Status.HTTP_BAD_FORBIDDEN

    new_viewer = request.form['new_viewer']
    comments = Comments.query.filter(Comments.parent_image == image.id).order_by(Comments.timestamp)
    owner = True

    port = str(os.environ.get('$PORT', 8080))
    image_route = "https://screenshot-tool-eecs498.herokuapp.com/api/get-image?id=" + str(image.id)

    if new_viewer == image.owner:
        options = {
            'user': user,
            'image': image,
            'comments': comments,
            'owner': owner,
            'image_route': image_route,
            'add_viewer_message': "User " + new_viewer + " is the owner of this image"
        }
        return render_template('details.html', **options), Status.HTTP_BAD_REQUEST

    if Viewable.query.filter(Viewable.image_name == image.name and Viewable.user_name == new_viewer).first():
        options = {
            'user': user,
            'image': image,
            'comments': comments,
            'owner': owner,
            'image_route': image_route,
            'add_viewer_message': "User " + new_viewer + " already has permission to view this image"
        }
        return render_template('details.html', **options), Status.HTTP_BAD_REQUEST

    db.session.add(Viewable(
        image_name=image.name, image_id=image.id, user_name=new_viewer
        ))
    db.session.commit()

    options = {
        'user': user,
        'image': image,
        'comments': comments,
        'owner': owner,
        'image_route': image_route,
        'add_viewer_message': "Succcessfully granted permission to " + new_viewer
    }
    return render_template('details.html', **options), Status.HTTP_OK_BASIC

def add_comment(request, user, image):
    owner = True
    if image.owner != user.username:
        owner = False

    port = str(os.environ.get('$PORT', 8080))
    image_route = "http://0.0.0.0:" + port + "/api/get-image?id=" + str(image.id)

    new_comment = request.form['comment']

    db.session.add(Comments(
        parent_image=image.id, author=user.username, comment_string=new_comment
        ))
    db.session.commit()

    comments = Comments.query.filter(Comments.parent_image == image.id).order_by(Comments.timestamp)

    options = {
        'user': user,
        'image': image,
        'comments': comments,
        'owner': owner,
        'image_route': image_route,
        'add_viewer_message': ""
    }
    return render_template('details.html', **options), Status.HTTP_OK_BASIC

def image_details_get(request, session):
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
            'message': 'image_id query parameter not specified'
        }
        return render_template('error.html', **options), Status.HTTP_BAD_REQUEST

    image_id = query_params['image_id'][0]
    image = Image.query.filter(Image.id == image_id).first()

    if not image:
        options = {
            'user': user,
            'message': 'Image not found'
        }
        return render_template('error.html', **options), Status.HTTP_BAD_NOTFOUND

    owner = True

    if image.owner != username:
        owner = False

        if not Viewable.query.filter(Viewable.image_name == image.name and Viewable.user_name == username).first():
            options = {
                'user': user,
                'message': 'You do not own this image or have permission to view it'
            }
            return render_template('error.html', **options), Status.HTTP_BAD_FORBIDDEN

    comments = Comments.query.filter(Comments.parent_image == image.id).order_by(Comments.timestamp)

    port = str(os.environ.get('$PORT', 8080))
    image_route = "http://0.0.0.0:" + port + "/api/get-image?id=" + str(image.id)

    options = {
        'user': user,
        'image': image,
        'comments': comments,
        'owner': owner,
        'image_route': image_route,
        'add_viewer_message': ""
    }
    return render_template('details.html', **options), Status.HTTP_OK_BASIC

def image_details_post(request, session):
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
            'message': 'image_id query parameter not specified'
        }
        return render_template('error.html', **options), Status.HTTP_BAD_NOTFOUND

    if 'action' not in query_params:
        options = {
            'user': user,
            'message': 'action query parameter not specified'
        }
        return render_template('error.html', **options), Status.HTTP_BAD_REQUEST

    image_id = query_params['image_id'][0]
    image = Image.query.filter(Image.id == image_id).first()

    if not image:
        options = {
            'user': user,
            'message': 'Image not found'
        }
        return render_template('error.html', **options), Status.HTTP_BAD_NOTFOUND

    action = int(query_params['action'][0])

    if action != 0 and action != 1:
        options = {
            'user': user,
            'message': 'Invalid action specified'
        }
        return render_template('error.html', **options), Status.HTTP_BAD_REQUEST

    if action == 0:
        return add_viewer(request, user, image)
    elif action == 1:
        return add_comment(request, user, image)
    else:
        options = {
            'user': user,
            'message': 'Action was not 0 or 1. It should never get here'
        }
        return render_template('error.html', **options), 500

@details_blueprint.route('/details', methods=['GET', 'POST'])
def image_details():
    if request.method == 'GET':
        return image_details_get(request, session)
    else:
        return image_details_post(request, session)
