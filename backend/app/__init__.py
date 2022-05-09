from flask import Flask, make_response, request
from flask_cors import CORS
from flask_migrate import Migrate
from flask_socketio import SocketIO, emit

from .accounts.accounts import accounts
from .accounts.models import User
from .common import db, mail, jwt

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
db.init_app(app)
migrate = Migrate(app, db)
mail.init_app(app)
jwt.init_app(app)


socketio = SocketIO()
socketio.init_app(app, cors_allowed_origins='http://127.0.0.1:8080', async_mode='threading')


def auth_only(func):
    def decorator():
        print(request.headers.get("access_token"))
        func()

    return decorator


@socketio.on('connect')
@auth_only
def test_connect():
    emit("event", "TEST")
    print("connect")


@socketio.on('disconnect')
def test_disconnect():
    print("disconnect")


@socketio.on('event')
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


with app.app_context():
    try:
        print(*(f"{u.to_dict()}\n" for u in db.session.query(User).all()))
        db.create_all()
        db.session.add(User(username="root41", name="Vladislav", email="heamongus@mail.ru", password="Root_41"))
        db.session.add(User(username="user41", name="FirstUser", email="user1@mail.ru", password="Root_41"))
        db.session.commit()
    except Exception:
        pass


@app.route("/", methods=['get'])
def index():
    res = make_response({"Message": "Hello world"}, 200)
    return res




