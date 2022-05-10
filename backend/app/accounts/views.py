import json

from flask import make_response, request
from flask import current_app as app

from app.accounts import accounts
from app.accounts.models import User
from app.accounts.utils import TwoFactorAuthentication
from app.accounts.my_jwt import MyJWT
from app.accounts.custom_error import *
from app.accounts.validator import UserValidator


@accounts.route('/login/', methods=['post'])
def login():
    data = request.get_json()
    username = data.get('username', None)
    password = data.get('password', None)

    if not (username and password and UserValidator.is_valid_username_and_password(username, password)):
        return make_response({"Error": "Invalid username or password"}, 404)

    user = User.authenticate(username=username, password=password)

    if not user:
        return make_response({"Error": "Invalid username or password"}, 404)

    otp_number = data.get('OTPNumber', 0)

    if not otp_number:
        TwoFactorAuthentication.authenticate_with_email(user)
        return make_response({"Message": "OTP number was send on your email"}, 200)

    if UserValidator.is_valid_otp_number(otp_number):
        try:
            user_otp_number = user.get_otp_number()
        except OTPTryError as e:
            return make_response({"Error": f"{e}"}, 404)
        if user_otp_number == otp_number or app.config.get("DEBUG"):
            user.otp_try = 3
            response = make_response({})

            access_token = MyJWT.encode_token(user.username, token_type="access")
            refresh_token = MyJWT.encode_token(user.username, token_type="refresh")
            MyJWT.set_cookie(response, access_token, token_type="access")
            MyJWT.set_cookie(response, refresh_token, token_type="refresh")

            response.data = json.dumps({'Message': 'Login successfully',
                                        'access_token': access_token,
                                        'refresh_token': refresh_token})
            return response
        else:
            return make_response({"Error": "Invalid OTP number"}, 404)
    else:
        TwoFactorAuthentication.authenticate_with_email(user)
        return make_response({"Message": "OTP number was send on your email"}, 200)


@accounts.route("/logout/", methods=["DELETE"])
@MyJWT.jwt_required()
def logout():
    response = make_response({"Message": "logout successful"})
    MyJWT.unset_cookie(response, "access")
    MyJWT.unset_cookie(response, "refresh")
    return response


@accounts.route("/refresh/", methods=['post'])
@MyJWT.jwt_required(token_type="refresh")
def refresh():
    response = make_response({"Message": "token was refreshed"})
    refresh_token = request.cookies.get('refresh_token')
    username = MyJWT.get_username_from_jwt(refresh_token, token_type='refresh')
    access_token = MyJWT.encode_token(username=username, token_type='access')
    MyJWT.set_cookie(response, access_token, token_type='access')
    return response


@accounts.route("/user/")
@MyJWT.jwt_required()
def get_user_info():
    token = request.cookies.get("access_token")
    return make_response(MyJWT.get_current_user(token, token_type='access').to_dict())
