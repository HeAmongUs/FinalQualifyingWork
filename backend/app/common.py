from flask_socketio import SocketIO
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
mail = Mail()
jwt = JWTManager()
socketio = SocketIO()

