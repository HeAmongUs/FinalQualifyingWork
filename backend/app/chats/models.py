from datetime import datetime

from ..common import db
from ..accounts.models import User

users = db.Table('users',
                 db.Column('user_username', db.Integer, db.ForeignKey('user.username')),
                 db.Column('chat_id', db.Integer, db.ForeignKey('chat.id'))
                 )


class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), unique=True, nullable=False)
    # one Chat to many messages
    messages = db.relationship('Message', backref='chat', lazy='dynamic')
    # many USERS to many CHATS
    users_in_chat = db.relationship('User', secondary=users,
                                    backref=db.backref('chats', lazy='dynamic'))

    def __repr__(self):
        return f'Chat: {self.id}: {self.title}'

    @property
    def serialize(self):
        return {
            "id": self.id,
            "title": self.title
        }


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(2500), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)

    # Foreign key
    user_username = db.Column(db.Integer, db.ForeignKey('user.username'))
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'))

    def __repr__(self):
        return f'MSG: {self.id}: {self.text}'

    @property
    def serialize(self):
        return {
            "id": self.id,
            "username": self.user_username,
            "text": self.text,
            "created": self.created_on
        }
