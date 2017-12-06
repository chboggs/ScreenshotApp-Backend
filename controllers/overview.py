import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from flask import *
from models import User
from factory import db
from http_codes import *

overview_blueprint = Blueprint('overview_blueprint', __name__, template_folder='templates')

@overview_blueprint.route('/overview', methods=['GET'])
def account_overview():
    if 'username' not in session:
        return redirect(url_for('login_blueprint.login_user'))

    user = session['username']
    return render_template('overview.html')
