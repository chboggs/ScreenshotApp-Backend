from flask import *
from ..models import User
from ..factory import db
from ..http_codes import *

new_user = Blueprint('new_user', __name__, template_folder='templates')

@user.route('/new-user', methods=['POST'])
def new_user():
    params = request.get_json()
    username = params.get('username', None)
    password = params.get('password', None)
    first_name = params.get('first_name', None)
    last_name = params.get('last_name', None)
    email = params.get('email', None)

    if not username or not password or not first_name or not last_name or not email:
        # TODO
        pass

    m = hashlib.new('sha512')
    m.update(password.encode('utf-8'))
    password = m.hexdigest()

    if User.query.filter(User.username == username).first() or User.query.filter(User.email == email).first():
        # TODO
        pass

    db.session.add(User(
        username=username, email=email, password=password, first_name=first_name, last_name=last_name
        ))
    db.session.commit()

    # TODO
    # return jsonify({"msg": "Successfully created user"}), Status.HTTP_OK_BASIC
