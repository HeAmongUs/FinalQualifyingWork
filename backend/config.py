import os
import secret
from datetime import timedelta

app_dir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY') or secret.SECRET_KEY
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ALLOWED_HOSTS = "*"
    CORS_HEADERS = 'Content-Type'

    # Config Flask-Mail
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME") or secret.MAIL_USERNAME
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or secret.MAIL_PASSWORD
    MAIL_SERVER = 'smtp.mail.ru'
    MAIL_PORT = 2525
    MAIL_USE_TLS = True
    MAIL_DEFAULT_SENDER = MAIL_USERNAME

    # config for field 'password' in accounts.models.User
    NAME_MIN_LENGTH = 6
    USERNAME_MIN_LENGTH = 6
    PASSWORD_MIN_LENGTH = 6
    PASSWORD_INCLUDES_SPECIAL_SYMBOLS = True
    PASSWORD_INCLUDES_LOWERCASE = True
    PASSWORD_INCLUDES_UPPERCASE = True
    PASSWORD_INCLUDES_DIGITS = True
    ALLOWED_SPECIAL_SYMBOLS = '!#%+-*/<=>?@[]^_|~'

    # JWT
    JWT_ISSUER_NAME = 'backend_server'
    JWT_AUDIENCE_LIST = ['frontend_client', 'mobile_client']
    JWT_IDENTITY_CLAIM = "username"

    JWT_ACCESS_TOKEN_COOKIE_NAME = "access_token"
    JWT_ACCESS_TOKEN_COOKIE_PATH = "/"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=6)

    JWT_REFRESH_TOKEN_COOKIE_NAME = "refresh_token"
    JWT_REFRESH_TOKEN_COOKIE_PATH = "/api/v1/accounts/refresh"
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

    JWT_COOKIE_DOMAIN = None
    JWT_COOKIE_SAMESITE = 'None'
    JWT_COOKIE_SECURE = False
    JWT_COOKIE_HTTP_ONLY = True
    JWT_SESSION_COOKIE = False
    JWT_COOKIE_CSRF_PROTECT = False


class Config(BaseConfig):
    DEBUG = True
    # DATABASE_NAME = os.environ.get("DATABASE_NAME")
    # DATABASE_USER = os.environ.get("DATABASE_USER")
    # DATABASE_USER_PASSWORD = os.environ.get("DATABASE_USER_PASSWORD")
    # DATABASE_ROOT = os.environ.get("DATABASE_ROOT")
    # DATABASE_ROOT_PASSWORD = os.environ.get("DATABASE_ROOT_PASSWORD")
    # SQLALCHEMY_DATABASE_URI = f"postgresql://{DATABASE_USER}:{DATABASE_USER_PASSWORD}@localhost:5432/{DATABASE_NAME}"

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(app_dir, 'app.db')


# ИАФ 4 усиление
# Class | Min-Len | ALPH | Trys | LockTimeMin | ChangePasswordDays |
# 4     |    6    | >30  | 3-10 | 3-15        | <=180              |
# 3     |    6    | >60  | 3-10 | 5-30        | <=120              |
# 2     |    6    | >70  | 3-8  | 10-30       | <=90               |
# 1     |    8    | >70  | 3-4  | 15-60       | <=60               |
