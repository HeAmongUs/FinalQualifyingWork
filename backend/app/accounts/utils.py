import re
import secrets
from hashlib import sha256
from string import ascii_lowercase, ascii_uppercase, digits

from flask_mail import Message

from flask import current_app as app
from ..common import db, mail


class UserPassword:
    @staticmethod
    def get_random_salt() -> str:
        return secrets.token_hex(8)

    @staticmethod
    def get_hash(password: str, salt: str) -> str:
        password_sting = password + salt
        return sha256(password_sting.encode()).hexdigest()

    @staticmethod
    def check_hash(password_hash: str, password: str, salt: str) -> bool:
        password_sting = password + salt
        return sha256(password_sting.encode()).hexdigest() == password_hash


class UserValidator:
    # User.name
    @staticmethod
    def is_valid_name(name: str) -> bool:
        return True

    # User.username
    @staticmethod
    def is_valid_username(username: str) -> bool:
        return True

    # User.email
    @staticmethod
    def is_valid_email(email: str) -> bool:
        if re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
            return True
        raise InvalidEmailError

    # User.password
    @staticmethod
    def __is_valid_password_length(password: str) -> bool:
        is_valid_password_length = len(password) >= app.config.get('PASSWORD_MIN_LENGTH', 0)

        if not is_valid_password_length:
            raise PasswordMinLengthError
        return True

    @staticmethod
    def __is_valid_password_lowercase(password):
        if app.config.get("PASSWORD_INCLUDES_LOWERCASE", False):
            for char in password:
                if char in ascii_lowercase:
                    return True
            raise PasswordIncludeLowercaseError
        else:
            return True

    @staticmethod
    def __is_valid_password_uppercase(password):
        if app.config.get("PASSWORD_INCLUDES_UPPERCASE", False):
            for char in password:
                if char in ascii_uppercase:
                    return True
            raise PasswordIncludeUppercaseError
        else:
            return True

    @staticmethod
    def __is_valid_password_digit(password):
        if app.config.get("PASSWORD_INCLUDES_DIGITS", False):
            for char in password:
                if char in digits:
                    return True
            raise PasswordIncludeDigitsError
        else:
            return True

    @staticmethod
    def __is_valid_password_special_symbols(password):
        if app.config.get("PASSWORD_INCLUDES_SPECIAL_SYMBOLS", False):
            for char in password:
                if char in app.config.get("ALLOWED_SPECIAL_SYMBOLS"):
                    return True
            raise PasswordIncludeSpecialSymbolError
        else:
            return True

    @classmethod
    def is_valid_password(cls, password):
        return all([
            cls.__is_valid_password_length(password),
            cls.__is_valid_password_lowercase(password),
            cls.__is_valid_password_uppercase(password),
            cls.__is_valid_password_digit(password),
            cls.__is_valid_password_special_symbols(password),
        ])

    # User.otp_number
    @staticmethod
    def is_valid_otp_number(otp_number):
        return 100000 <= int(otp_number) < 1000000


class TwoFactorAuthentication:
    @staticmethod
    def get_OTP_number():
        return "".join(secrets.choice("0123456789") for i in range(6))

    @staticmethod
    def send_OTP_number(email, otp_number):
        msg = Message("Verification code", recipients=[f'{email}'])
        msg.html = \
            f"<h1>Verification code</h1>" \
            f"<p>An attempt was made to log into your account</p>" \
            f"<p>Your code: {otp_number}</p>"

        if not app.config.get("DEBUG"):
            mail.send(msg)

    @staticmethod
    def authenticate_with_email(user):
        try:
            user.set_otp_number(TwoFactorAuthentication.get_OTP_number())
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            raise Exception(f'{e}, \n authenticate_with_email')
        TwoFactorAuthentication.send_OTP_number(user.get_email(), user.get_otp_number())


class PasswordMinLengthError(Exception):
    def __str__(self):
        return 'The entered password is shorter than the allowed length'


class InvalidEmailError(Exception):
    def __str__(self):
        return 'The entered email is invalid'


class PasswordIncludeLowercaseError(Exception):
    def __str__(self):
        return 'The entered password must includes one of lowercase letter'


class PasswordIncludeUppercaseError(Exception):
    def __str__(self):
        return 'The entered password must includes one of uppercase letter'


class PasswordIncludeDigitsError(Exception):
    def __str__(self):
        return 'The entered password must includes one of digit'


class PasswordIncludeSpecialSymbolError(Exception):
    def __str__(self):
        return f'The entered password must includes one of special character: \n' \
               f'{app.config.get("ALLOWED_SPECIAL_SYMBOLS")}'
