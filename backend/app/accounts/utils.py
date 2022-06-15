import secrets
from hashlib import sha256

from flask_mail import Message
from flask import current_app as app

from .custom_error import OTPTryError
from app.common import db, mail


class HashPassword:
    @staticmethod
    def get_random_salt() -> str:
        return secrets.token_hex(8)

    @staticmethod
    def get_hash(password: str, salt: str) -> str:
        password_sting = password + salt
        return sha256(password_sting.encode()).hexdigest()

    @staticmethod
    def check_hash(password_hash: str, password: str, salt: str) -> bool:
        return HashPassword.get_hash(password, salt) == password_hash


class TwoFactorAuthentication:
    @staticmethod
    def get_OTP_number():
        return int("".join(secrets.choice("0123456789") for i in range(6)))

    @staticmethod
    def send_OTP_number(email, otp_number):
        msg = Message("Verification code", recipients=[f'{email}'])
        msg.html = \
            f"<h1>Verification code</h1>" \
            f"<h5>An attempt was made to log into your account</h5>" \
            f"<p>Your code: <strong>{otp_number}</strong> </p>"

        if not app.config.get("DEBUG"):
            mail.send(msg)

    @staticmethod
    def authenticate_with_email(user):
        try:
            user.set_otp_number(TwoFactorAuthentication.get_OTP_number())
            TwoFactorAuthentication.send_OTP_number(user.get_email(), user.otp_number)
            user.clear_otp_try()
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            raise Exception(f'{e}, \n error authenticate_with_email')


def otp_try(user):
    if user.otp_try < app.config.get("OTP_TRY_COUNT", 3):
        user.otp_try += 1
        db.session.add(user)
        db.session.commit()
        return user.otp_number
    else:
        raise OTPTryError
