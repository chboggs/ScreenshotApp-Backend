import os, sys, inspect
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
    if request.method == 'GET':
        if 'username' in session:
            return redirect(url_for('overview_blueprint.account_overview'))
        else:
            options = {
                "error": False
            }
            return render_template('login.html', **options)
    else:
        username = request.form['username']
        password = request.form['password']
        if username == "":
            if password == "":
                options = {
                    "error": True,
                    "problem": {"Username may not be left blank", "Password may not be left blank"}
                }
                return render_template("login.html", **options)
            options = {
                "error": True,
                "problem": {"Username may not be left blank"}
            }
            return render_template("login.html", **options)
        if password == "":
            options = {
                "error": True,
                "problem": {"Password may not be left blank"}
            }
            return render_template("login.html", **options)

        print('Username received: ' + username)
        print('Password received: ' + password)

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
        # session['username'] = username
        # return redirect(url_for('overview_blueprint.account_overview'))
