import json

from flask import make_response, request
from flask import current_app as app

from app.accounts import accounts
from app.accounts.models import User
from app.accounts.utils import TwoFactorAuthentication
from app.accounts.my_jwt import MyJWT
from app.accounts.custom_error import *
from app.accounts.validator import UserValidator

from ..common import db


@accounts.route('/login', methods=['post'])
def login():
    data = request.get_json()
    username = data.get('username', None)
    password = data.get('password', None)

    if not UserValidator.is_valid_username_and_password(username, password):
        return make_response({"Error": "Invalid username or password"}, 403)

    user = User.authenticate(username=username, password=password)

    if not user:
        return make_response({"Error": "Invalid username or password"}, 403)

    otp_number = data.get('OTPNumber', 0)

    if not otp_number:
        TwoFactorAuthentication.authenticate_with_email(user)
        return make_response({"Message": "OTP number was send on your email"}, 200)

    if not UserValidator.is_valid_otp_number(otp_number):
        return make_response({"Message": "OTP number number is invalid"}, 403)

    try:
        user_otp_number = user.get_otp_number()
        print(user.otp_try)
    except OTPTryError as e:
        return make_response({"Error": f"OTP try error. New code was send on your email"}, 403)

    if not (user_otp_number == otp_number or app.config.get("DEBUG")):
        return make_response({"Error": "OTP number number is invalid"}, 403)

    user.otp_try = 3
    db.session.commit()

    access_token = MyJWT.encode_token(user.username, token_type="access")
    refresh_token = MyJWT.encode_token(user.username, token_type="refresh")

    return make_response({'Message': 'Login successfully',
                          'access_token': access_token,
                          'refresh_token': refresh_token}, 200)


@accounts.route("/logout", methods=["DELETE"])
@MyJWT.jwt_required()
def logout():
    response = make_response({"Message": "logout successful"})
    return response


@accounts.route("/refresh", methods=['POST'])
@MyJWT.jwt_required(token_type="refresh")
def refresh():
    refresh_token = MyJWT.get_token_from_request(token_type="refresh")
    username = MyJWT.get_username_from_jwt(refresh_token, token_type='refresh')
    access_token = MyJWT.encode_token(username=username, token_type='access')
    return json.dumps({"Message": "token was refreshed",
                       'access_token': access_token,
                       'refresh_token': refresh_token})


@accounts.route("/user")
@MyJWT.jwt_required()
def get_user_info():
    return make_response(MyJWT.get_current_user(token_type='access').to_dict())
