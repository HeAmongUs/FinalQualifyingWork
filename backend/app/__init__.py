from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_socketio import emit

from app.accounts import accounts, MyJWT
from app.accounts.models import User
from app.common import db, mail, jwt, socketio

from app.chats import chats


@socketio.on('connect')
def test_connect():
    emit("event", "TEST")
    print("connect")


@socketio.on('disconnect')
def test_disconnect():
    print("disconnect")


@socketio.on('disconnecting')
def test_disconnecting():
    print("disconnecting")


@socketio.on('event')
@MyJWT.jwt_required()
def message(msg):
    print(f"MSG: {msg}")


@jwt.user_lookup_loader
def user_loader_callback(jwt_header, jwt_payload):
    """Function for app, to return user object"""
    if jwt_header:
        username = jwt_payload["username"]
        user = User.query.filter_by(username=username).one_or_none()
        return user
    return None


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    app.debug = app.config.get("DEBUG")
    cors = CORS(
        app,
        supports_credentials=True,
        resources={
            r'/': {'origins': ['http://127.0.0.1:8080', 'http://localhost:8080']},
            r'/api/v1/*': {'origins': ['http://127.0.0.1:8080', 'http://localhost:8080']},
        })
    app.register_blueprint(accounts)
    app.register_blueprint(chats)
    db.init_app(app)
    migrate = Migrate(app, db)
    mail.init_app(app)
    jwt.init_app(app)
    socketio.init_app(app, cors_allowed_origins='http://127.0.0.1:8080', async_mode='threading')

    with app.app_context():
        try:
            db.create_all()
            db.session.add(User(username="root41", name="Vladislav", email="heamongus@mail.ru", password="Root_41"))
            db.session.add(User(username="user41", name="FirstUser", email="user1@mail.ru", password="Root_41"))
            db.session.commit()
        except Exception:
            pass

    return socketio, app




