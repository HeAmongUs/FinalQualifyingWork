from flask import Blueprint

accounts = Blueprint('accounts', __name__, url_prefix='/api/v1/accounts')

from .views import *
