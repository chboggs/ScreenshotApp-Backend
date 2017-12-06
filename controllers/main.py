from flask import *

main_blueprint = Blueprint('main_blueprint', __name__, template_folder='templates')

@main_blueprint.route('/')
def main_route():
    if 'username' in session:
        return redirect(url_for('overview_blueprint.user_overview'))
    else:
        return redirect(url_for('login_blueprint.login_user'))
