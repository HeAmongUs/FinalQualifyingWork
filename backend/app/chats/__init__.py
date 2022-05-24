from flask import Blueprint

chats = Blueprint('chats', __name__, url_prefix='/api/v1/chats')

from .views import *
