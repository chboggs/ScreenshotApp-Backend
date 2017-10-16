# // ./app.py

from flask import Flask, request
from flask_mail import Mail, Message

DEBUG = True
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = 'ar6screenshot@gmail.com'
MAIL_PASSWORD = 'alexchrischristophcody'


app = Flask(__name__)
app.config.from_object(__name__)
mail = Mail(app)

@app.route('/health')
def health():
	return 'Status: Healthy'

@app.route('/')
def hello():
	return "Welcome to AR-6's screenshot app!"

@app.route('/new-image', methods=['POST'])
def new_image():
	content = request.form
	subject = "New Image!"
	recipients = ["ar6screenshot@gmail.com"]
	if "subject" in content:
		subject = content["subject"]
	if "recipient" in content:
		recipients.append(content["recipient"])
	new_im = request.files['image']
	file_name = new_im.filename
	msg = Message(subject, sender="ar6screenshot@gmail.com", recipients=recipients)
	msg.attach(file_name, new_im.content_type, new_im.stream.read())
	if "body" in content:
		msg.body = content["body"]

	mail.send(msg)
	return 'Success', 200


if __name__ == "__main__":
	app.run()