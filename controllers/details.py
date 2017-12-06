import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from flask import *
from models import User
from factory import db
from http_codes import *

details_blueprint = Blueprint('details_blueprint', __name__, template_folder='templates')

@details_blueprint.route('/details', methods=['GET'])
def image_details():
    print("Got to details page")
