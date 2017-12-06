from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/app.db'
app.secret_key = 'ghblidrgbwlier7yuio4h398'

db = SQLAlchemy()
db.init_app(app)

cur_dir = os.getcwd()
image_dir = os.path.join(cur_dir, 'images')
relative_image_dir = "/images"
