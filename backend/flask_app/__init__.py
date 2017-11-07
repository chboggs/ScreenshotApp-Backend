from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
	app = Flask(__name__)
	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/app.db'
	app.secret_key = 'ghblidrgbwlier7yuio4h398'
	# app.config['SESSION_TYPE'] = 'sqlalchemy'

	db.init_app(app)

	return app
