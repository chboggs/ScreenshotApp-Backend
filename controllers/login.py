import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from flask import *
from models import User
from factory import db
from http_codes import *

login_blueprint = Blueprint('login_blueprint', __name__, template_folder='templates')

@login_blueprint.route('/login', methods=['POST'])
def login_user():
    params = request.get_json()
    username = params.get('username', None)
    password = params.get('password', None)

    if not username or not password:
        # TODO
        pass

    m = hashlib.new('sha512')
    m.update(password.encode('utf-8'))
    password = m.hexdigest()

    registered_user = User.query.filter(User.username == username, User.password == password).first()

    if not registered_user:
        # TODO
        pass

    # TODO
    session['username'] = username
    return redirect(url_for('overview.account_overview'))
