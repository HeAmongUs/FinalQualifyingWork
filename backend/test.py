import jwt
import unittest

from app import create_app
from app.accounts.my_jwt import MyJWT


class MyJWTTest(unittest.TestCase):
    def setUp(self) -> None:
        self.socket, self.app = create_app()

    def test_token_type(self):
        with self.app.app_context():
            expected = "access"
            token = MyJWT.encode_token("HeAmongUs", token_type=expected)
            actual = jwt.get_unverified_header(token).get("typ", '')
            self.assertEqual(actual, expected)

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
