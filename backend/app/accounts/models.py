from datetime import datetime

from flask_login import UserMixin

from ..common import db
from .utils import UserPassword, UserValidator


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    otp_number = db.Column(db.Integer)
    password_hash = db.Column(db.String(100), nullable=False)
    password_salt = db.Column(db.String(100))
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, name, username, email, password):
        self.set_name(name)
        self.set_username(username)
        self.set_email(email)
        self.set_password(password)

    @classmethod
    def authenticate(cls, **kwargs):
        username = kwargs.get('username')
        password = kwargs.get('password')

        if not username or not password:
            return None

        user = cls.query.filter_by(username=username).first()
        if not user or not UserPassword.check_hash(user.password_hash, password, user.password_salt):
            return None

        return user

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.username)

    def to_dict(self):
        return dict(id=self.id, name=self.name, username=self.username, email=self.email)

    def set_name(self, name):
        if UserValidator.is_valid_name(name):
            self.name = name

    def set_username(self, username):
        if UserValidator.is_valid_username(username):
            self.username = username

    def set_email(self, email):
        if UserValidator.is_valid_email(email):
            self.email = email

    def set_password(self, password):
        if UserValidator.is_valid_password(password):
            self.password_salt = UserPassword.get_random_salt()
            self.password_hash = UserPassword.get_hash(password, self.password_salt)

    def set_otp_number(self, otp_number):
        if UserValidator.is_valid_otp_number(otp_number):
            self.otp_number = otp_number

    def get_otp_number(self):
        return self.otp_number

    def get_email(self):
        return self.email
