from flask import Blueprint, make_response, request
from flask_jwt_extended import create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies, \
    unset_jwt_cookies, jwt_required, get_current_user
from flask import current_app as app

from .models import User
from .utils import UserValidator, TwoFactorAuthentication
from .custom_error import *

accounts = Blueprint('accounts', __name__, url_prefix='/api/v1/accounts')


@accounts.route('/login/', methods=['post'])
def login():
    data = request.get_json()
    username = data.get('username', None)
    password = data.get('password', None)
    is_valid = False
    if username and password:
        try:
            is_valid = UserValidator.is_valid_username_and_password(username, password)
        except (PasswordMinLengthError,
                PasswordIncludeLowercaseError,
                PasswordIncludeUppercaseError,
                PasswordIncludeDigitsError,
                PasswordIncludeSpecialSymbolError) as e:
            return make_response({"Error": f"{e}"}, 404)

    if is_valid:
        user = User.authenticate(username=username, password=password)
        if user:
            otp_number = data.get('OTPNumber', 0)
            if otp_number and UserValidator.is_valid_otp_number(otp_number):
                try:
                    user_otp_number = user.get_otp_number()
                except OTPTryError as e:
                    return make_response({"Error": f"{e}"}, 404)
                if user_otp_number == otp_number or app.config.get("DEBUG"):
                    user.otp_try = 3
                    response = make_response({"Message": "Login successfully"}, 200)

                    access_token = create_access_token(identity=user.username)
                    refresh_token = create_refresh_token(identity=user.username)
                    set_access_cookies(response, access_token, max_age=app.config.get("JWT_ACCESS_TOKEN_EXPIRES"),)
                    set_refresh_cookies(response, refresh_token, max_age=app.config.get("JWT_REFRESH_TOKEN_EXPIRES"),)
                    return response
                else:
                    return make_response({"Error": "Invalid OTP number"}, 404)
            else:
                TwoFactorAuthentication.authenticate_with_email(user)
                return make_response({"Message": "OTP number was send on your email"}, 200)
        else:
            return make_response({"Error": "Invalid username or password"}, 404)
    return make_response({"Error": "Invalid username or password"}, 404)


@accounts.route("/logout/", methods=["DELETE"])
@jwt_required()
def logout():
    response = make_response({"Message": "logout successful"})
    unset_jwt_cookies(response)
    return response


@accounts.route("/refresh/", methods=['post'])
@jwt_required(refresh=True)
def refresh():
    response = make_response({"Message": "token was refreshed"})
    access_token = create_access_token(identity=get_current_user().username)
    set_access_cookies(response, access_token, max_age=app.config.get("JWT_ACCESS_TOKEN_EXPIRES"),)
    return response


@accounts.route("/user/")
@jwt_required()
def get_user_info():
    return make_response(get_current_user().to_dict())

