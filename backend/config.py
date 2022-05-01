import os
import secret
from datetime import timedelta

app_dir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'flask-secret-1234567890'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CORS_HEADERS = 'Content-Type'

    # Config Flask-Mail
    MAIL_USERNAME = secret.MAIL_USERNAME
    MAIL_PASSWORD = secret.MAIL_PASSWORD
    MAIL_SERVER = secret.MAIL_SERVER
    MAIL_PORT = secret.MAIL_PORT
    MAIL_USE_TLS = secret.MAIL_USE_TLS
    MAIL_DEFAULT_SENDER = MAIL_USERNAME

    # config for field 'password' in accounts.models.User
    PASSWORD_MIN_LENGTH = 6
    PASSWORD_INCLUDES_SPECIAL_SYMBOLS = True
    PASSWORD_INCLUDES_LOWERCASE = True
    PASSWORD_INCLUDES_UPPERCASE = True
    PASSWORD_INCLUDES_DIGITS = True
    ALLOWED_SPECIAL_SYMBOLS = "!#%+-*/<=>?@[\]^_{|}~"

    # JWT
    JWT_TOKEN_LOCATION = ('cookies',)
    JWT_IDENTITY_CLAIM = "username"
    JWT_COOKIE_DOMAIN = None
    JWT_COOKIE_SAMESITE = 'Lax'
    JWT_COOKIE_SECURE = False
    JWT_COOKIE_HTTP_ONLY = True
    JWT_SESSION_COOKIE = False
    JWT_COOKIE_CSRF_PROTECT = False

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=10)
    JWT_ACCESS_COOKIE_NAME = "access_token"
    JWT_ACCESS_COOKIE_PATH = "/"

    JWT_REFRESH_COOKIE_NAME = "refresh_token"
    JWT_REFRESH_COOKIE_PATH = "/api/v1/accounts/refresh/"
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)


class Config(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(app_dir, 'app.db')
    # f"postgresql://:{secret.DATABASE_USER}:{secret.DATABASE_PASSWORD}:5432/{secret.DATABASE_NAME} "

# ИАФ 4 усиление
# Class | Min-Len | ALPH | Trys | LockTimeMin | ChangePasswordDays |
# 4     |    6    | >30  | 3-10 | 3-15        | <=180              |
# 3     |    6    | >60  | 3-10 | 5-30        | <=120              |
# 2     |    6    | >70  | 3-8  | 10-30       | <=90               |
# 1     |    8    | >70  | 3-4  | 15-60       | <=60               |