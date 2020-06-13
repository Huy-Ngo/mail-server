from http import HTTPStatus as Http

from flask import Flask
from flask_restful import Resource, Api
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_json('config.json')

api = Api(app)
mail_service = Mail(app)
db = SQLAlchemy(app)


class MailModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipient = db.Column(db.String(254))
    message = db.Column(db.String)

    def __init__(self, recipient, message):
        self.recipient = recipient
        self.message = message

    def json(self):
        return {'id': self.id,
                'recipient': self.recipient,
                'message': self.message}


class MailStorage(Resource):
    def get(self):
        """Retrieve the sent mails."""
        all_mails = db.session.query().all()
        if all_mails is None:
            return {'status': Http.NOT_FOUND}
        return {'mails': [mail.json() for mail in all_mails],
                'status': Http.OK}

    def post(self, recipient, message):
        """Send email and save to the storage."""
        msg = Message(message, sender='', recipients=[recipient])
        mail_service.send(msg)
        sent_mail = MailModel(recipient, message)
        db.session.add(sent_mail)


api.add_resource(MailStorage, '/mail/')

if __name__ == '__main__':
    app.run(debug=True)
