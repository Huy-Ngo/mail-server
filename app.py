from flask import Flask
from flask_restful import Resource, Api
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
mail = Mail(app)

db = SQLAlchemy(app)


class MailStorage(Resource):
    def get(self):
        """Retrieve the sent mails."""
        pass

    def post(self):
        """Send email and save to the storage."""
        msg = Message('Testing email.', sender='', recipients=[])
        mail.send(msg)


api.add_resource(MailStorage, '/mail/')

if __name__ == '__main__':
    app.run(debug=True)
