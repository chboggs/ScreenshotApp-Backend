import os, sys, inspect, hashlib
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from flask import *
from models import User
from factory import db
from http_codes import *

login_blueprint = Blueprint('login_blueprint', __name__, template_folder='templates')

@login_blueprint.route('/login', methods=['POST', 'GET'])
def login_user():
    if 'username' in session:
        return redirect(url_for('overview_blueprint.user_overview')), Status.HTTP_OK_BASIC

    if request.method == 'GET':
        options = { "error": False }
        return render_template('login.html', **options), Status.HTTP_OK_BASIC
    else:
        username = request.form['username']
        password = request.form['password']

        if username == "":
            if password == "":
                options = {
                    "error": True,
                    "problem": { "Username may not be left blank", "Password may not be left blank" }
                }
                return render_template("login.html", **options), Status.HTTP_BAD_REQUEST
            options = {
                "error": True,
                "problem": { "Username may not be left blank" }
            }
            return render_template("login.html", **options), Status.HTTP_BAD_REQUEST
        if password == "":
            options = {
                "error": True,
                "problem": { "Password may not be left blank" }
            }
            return render_template("login.html", **options), Status.HTTP_BAD_REQUEST

        m = hashlib.new('sha512')
        m.update(password.encode('utf-8'))
        password = m.hexdigest()

        registered_user = User.query.filter(User.username == username, User.password == password).first()

        if not registered_user:
            options = {
                "error": True,
                "problem": { "Invalid login" }
            }
            return render_template("login.html", **options), Status.HTTP_BAD_UNAUTHORIZED

        session['username'] = username
        return redirect(url_for('overview_blueprint.user_overview')), Status.HTTP_OK_BASIC
