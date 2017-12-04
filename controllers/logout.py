from flask import *

logout_blueprint = Blueprint('logout_blueprint', __name__, template_folder='templates')

@logout_blueprint.route('/logout', methods=['POST'])
def logout_user():
	session.pop('username', None)
	return redirect(url_for('login.login_user'))
