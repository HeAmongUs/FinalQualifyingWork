import datetime
import jwt
from functools import wraps

from flask import make_response, request
from flask import current_app as app
from flask.wrappers import Response

from app.accounts.models import User


class MyJWT:
    @staticmethod
    def encode_token(username: str, token_type: str = "access", ):
        """Create token_type token by username"""
        if token_type not in ['access', 'refresh']:
            token_type = 'access'
        try:
            payload = {
                'iat': datetime.datetime.utcnow(),
                'exp':
                    datetime.datetime.utcnow() +
                    app.config.get(f'JWT_{token_type.upper()}_TOKEN_EXPIRES', datetime.timedelta(minutes=5)),
                'username': username,
            }
            if app.config.get('JWT_ISSUER_NAME', None):
                payload['iss'] = app.config.get('JWT_ISSUER_NAME')
            if app.config.get('JWT_AUDIENCE_LIST', None):
                payload['aud'] = app.config.get('JWT_AUDIENCE_LIST')

            return jwt.encode(
                payload,
                app.config.get('SECRET_KEY', ''),
                headers={"typ": token_type, },
                algorithm='HS256'
            )
        except jwt.InvalidAlgorithmError:
            print("InvalidAlgorithmError")

    @staticmethod
    def decode_token(token: str, token_type: str = "access", ) -> dict:
        """Check token"""
        if jwt.get_unverified_header(token).get("typ", '') == token_type:
            kwargs = {}
            if app.config.get('JWT_AUDIENCE_LIST', None):
                kwargs['audience'] = app.config.get('JWT_AUDIENCE_LIST')
            if app.config.get('JWT_ISSUER_NAME', None):
                kwargs['issuer'] = app.config.get('JWT_ISSUER_NAME')
            payload = jwt.decode(token, app.config.get('SECRET_KEY', ''), algorithms="HS256", **kwargs)
            if app.config.get("JWT_IDENTITY_CLAIM", None) and app.config.get("JWT_IDENTITY_CLAIM") in payload:
                return payload
            else:
                raise jwt.InvalidTokenError

    @staticmethod
    def set_cookie(response: Response, token: str, token_type: str = "access") -> None:
        token_type_upper = token_type.upper()
        response.set_cookie(
            key=app.config.get(f"JWT_{token_type_upper}_TOKEN_COOKIE_NAME"),
            value=token,
            max_age=app.config.get(f"JWT_{token_type_upper}_TOKEN_EXPIRES"),
            secure=app.config.get("JWT_COOKIE_SECURE"),
            httponly=app.config.get("JWT_COOKIE_HTTP_ONLY"),
            domain=app.config.get("JWT_COOKIE_DOMAIN", None),
            path=app.config.get(f"JWT_{token_type_upper}_TOKEN_COOKIE_PATH"),
            samesite=app.config.get("JWT_COOKIE_SAMESITE"),
        )

    @staticmethod
    def unset_cookie(response: Response, token_type: str = "access") -> None:
        token_type_upper = token_type.upper()
        response.set_cookie(
            key=app.config.get(f"JWT_{token_type_upper}_TOKEN_COOKIE_NAME"),
            value="",
            expires=1,
            secure=app.config.get("JWT_COOKIE_SECURE"),
            httponly=app.config.get("JWT_COOKIE_HTTP_ONLY"),
            domain=app.config.get("JWT_COOKIE_DOMAIN", None),
            path=app.config.get(f"JWT_{token_type_upper}_TOKEN_COOKIE_PATH"),
            samesite=app.config.get("JWT_COOKIE_SAMESITE"),
        )

    @staticmethod
    def jwt_required(token_type="access"):

        def wrapper(func):
            @wraps(func)
            def inner(*args, **kwargs):
                try:
                    access_token = request.cookies.get(app.config.get(f'JWT_{token_type.upper()}_TOKEN_COOKIE_NAME', None))
                    if access_token:
                        MyJWT.decode_token(access_token)
                        return func(*args, **kwargs)
                    data = request.get_json()
                    if data:
                        access_token = data.get(app.config.get(f'JWT_{token_type.upper()}_TOKEN_COOKIE_NAME', None))
                    if access_token:
                        MyJWT.decode_token(access_token)
                        return func(*args, **kwargs)
                    access_token = request.headers.get('Access-Token', None)
                    if access_token:
                        MyJWT.decode_token(access_token)
                        return func(*args, **kwargs)
                    else:
                        return make_response({'message': 'token is missing'}, 401)
                except jwt.ExpiredSignatureError:
                    print("expired token")
                    return make_response({'message': 'token is expired'}, 401)
                except (jwt.InvalidTokenError, jwt.DecodeError) as e:
                    print(f'token is invalid', e)
                    return make_response({'message': 'token is invalid'}, 401)

            return inner

        return wrapper

    @staticmethod
    def get_username_from_jwt(token: str, token_type: str = 'access'):
        return MyJWT.decode_token(token, token_type=token_type).get('username')

    @staticmethod
    def get_current_user(token, token_type: str = 'access'):
        username = MyJWT.get_username_from_jwt(token, token_type)
        return User.query.filter_by(username=username).first()
