from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/app.db'
app.secret_key = 'ghblidrgbwlier7yuio4h398'
# app.config['SESSION_TYPE'] = 'sqlalchemy'

db = SQLAlchemy()
db.init_app(app)
