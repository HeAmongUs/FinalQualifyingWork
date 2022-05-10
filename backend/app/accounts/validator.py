from re import match as re_match
from string import ascii_lowercase, ascii_uppercase, digits
from flask import current_app as app


class UserValidator:
    # User.name
    @staticmethod
    def is_valid_name(name: str) -> bool:
        if len(name) >= app.config.get("NAME_MIN_LENGTH", 0):
            return True
        else:
            return False

    # User.username
    @staticmethod
    def is_valid_username(username: str) -> bool:
        if len(username) >= app.config.get("USERNAME_MIN_LENGTH", 0):
            return True
        else:
            return False

    # User.email
    @staticmethod
    def is_valid_email(email: str) -> bool:
        if re_match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
            return True
        else:
            return False

    # User.password
    @staticmethod
    def __is_valid_password_length(password: str) -> bool:
        is_valid_password_length = len(password) >= app.config.get('PASSWORD_MIN_LENGTH', 0)

        if is_valid_password_length:
            return True
        else:
            return False

    @staticmethod
    def __is_valid_password_lowercase(password):
        if app.config.get("PASSWORD_INCLUDES_LOWERCASE", False):
            for char in password:
                if char in ascii_lowercase:
                    return True
            return False
        else:
            return True

    @staticmethod
    def __is_valid_password_uppercase(password):
        if app.config.get("PASSWORD_INCLUDES_UPPERCASE", False):
            for char in password:
                if char in ascii_uppercase:
                    return True
            return False
        else:
            return True

    @staticmethod
    def __is_valid_password_digit(password):
        if app.config.get("PASSWORD_INCLUDES_DIGITS", False):
            for char in password:
                if char in digits:
                    return True
            return False
        else:
            return True

    @staticmethod
    def __is_valid_password_special_symbols(password):
        if app.config.get("PASSWORD_INCLUDES_SPECIAL_SYMBOLS", False):
            for char in password:
                if char in app.config.get("ALLOWED_SPECIAL_SYMBOLS"):
                    return True
            return False
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

    @staticmethod
    def is_valid_username_and_password(username, password):
        return all([
            UserValidator.is_valid_username(username),
            UserValidator.is_valid_password(password),
        ])