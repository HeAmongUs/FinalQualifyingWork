from datetime import datetime

from ..common import db


class Chat(db.Model):
    __tablename__ = "chats"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    users = ''
    messages = ''

    def __init__(self,):
        pass

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.title)


class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    user = ''
    text = db.Column(db.String(2500), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)

    def __init__(self,):
        pass

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.user)

