from flask import *
from ..models import User
from ..factory import db
from ..http_codes import *

overview = Blueprint('overview', __name__, template_folder='templates')

@overview.route('/overview', methods=['GET'])
def account_overview:
    user = session['username']
