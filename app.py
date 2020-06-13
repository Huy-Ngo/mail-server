from http import HTTPStatus as Http

from flask import Flask
from flask_restful import Resource, Api
from flask_restful.reqparse import RequestParser
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
    parser = RequestParser()
    parser.add_argument('recipient', type=str, required=True)
    parser.add_argument('message', type=str, required=True)

    def get(self):
        """Retrieve the sent mails."""
        all_mails = db.session.query().all()
        if all_mails is None:
            return {'status': Http.NOT_FOUND}
        return {'mails': [mail.json() for mail in all_mails],
                'status': Http.OK}

    def post(self):
        """Send email and save to the storage."""
        data = MailStorage.parser.parse_args()
        recipient = data['recipient']
        message = data['message']
        msg = Message(message, recipients=[recipient])
        mail_service.send(msg)
        sent_mail = MailModel(recipient, message)
        db.session.add(sent_mail)
        return {'mail': sent_mail.json(),
                'status': Http.CREATED}


api.add_resource(MailStorage, '/mail/')


@app.before_first_request
def create_database():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)
