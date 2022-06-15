import datetime
import time

import jwt
import unittest

from flask import request, make_response

from app import create_app
from app.accounts.my_jwt import MyJWT


class MyJWTTest(unittest.TestCase):
    def setUp(self) -> None:
        self.socket, self.app = create_app()

    def test_token_access_type(self):
        with self.app.app_context():
            expected = "access"
            token = MyJWT.encode_token("HeAmongUs", token_type=expected)
            actual = jwt.get_unverified_header(token).get("typ", '')
            self.assertEqual(actual, expected)

    def test_token_refresh_type(self):
        with self.app.app_context():
            expected = "refresh"
            token = MyJWT.encode_token("HeAmongUs", token_type=expected)
            actual = jwt.get_unverified_header(token).get("typ", '')
            self.assertEqual(actual, expected)

    def test_on_decode_token(self):
        with self.app.app_context():
            encode_token = MyJWT.encode_token("HeAmongUs")
            MyJWT.decode_token(encode_token)

    def test_get_username_from_jwt(self):
        with self.app.app_context():
            encode_token = MyJWT.encode_token("HeAmongUs")
            username = MyJWT.get_username_from_jwt(encode_token)
            self.assertEqual(username, "HeAmongUs")

    def test_get_user_from_jwt(self):
        with self.app.app_context():
            encode_token = MyJWT.encode_token("root41")
            with self.app.test_request_context('', headers={
                "Authorization": encode_token
            }):
                user = MyJWT.get_current_user()
                self.assertEqual(user.username, "root41")

    def test_jwt_required(self):
        with self.app.app_context():
            encode_token = MyJWT.encode_token("root41")
            with self.app.test_request_context('', headers={
                "Authorization": encode_token
            }):
                self.assertEqual(required_test(request).status_code, 200)

    def test_jwt_expired(self):
        with self.app.app_context():
            self.app.config[f"JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(seconds=1)
            encode_token = MyJWT.encode_token("root41")
            time.sleep(2)
            with self.app.test_request_context('', headers={
                "Authorization": encode_token
            }):
                self.assertEqual(required_test(request).get_json().get("message"), "token is expired")

    def test_jwt_invalid(self):
        with self.app.app_context():
            encode_token = MyJWT.encode_token("root41")
            with self.app.test_request_context('', headers={
                "Authorization": encode_token + "1"
            }):
                self.assertEqual(required_test(request).get_json().get("message"), "token is invalid")

    def test_jwt_missing(self):
        with self.app.app_context():
            with self.app.test_request_context(''):
                self.assertEqual(required_test(request).get_json().get("message"), "token is missing")

    def test_expired_access_token(self):
        with self.app.app_context():
            self.app.config[f"JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(seconds=1)
            encode_token = MyJWT.encode_token("HeAmongUs")
            time.sleep(2)
            with self.assertRaises(jwt.exceptions.ExpiredSignatureError):
                MyJWT.decode_token(encode_token)

    def test_expired_refresh_token(self):
        with self.app.app_context():
            self.app.config[f"JWT_REFRESH_TOKEN_EXPIRES"] = datetime.timedelta(seconds=1)
            encode_token = MyJWT.encode_token("HeAmongUs", token_type="refresh")
            time.sleep(2)
            with self.assertRaises(jwt.exceptions.ExpiredSignatureError):
                MyJWT.decode_token(encode_token, token_type="refresh")


@MyJWT.jwt_required()
def required_test(request):
    return make_response({}, 200)

