from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Contact(db.Model):
    __tablename__ = 'contacts'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True)
    topic = db.Column(db.String(50))
    message = db.Column(db.String(255))

    def __init__(self, name=None, email=None, topic=None, message=None):
        self.name = name
        self.email = email
        self.topic = topic
        self.message = message
