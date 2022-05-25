from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_socketio import emit

from app.accounts import accounts
from app.accounts.my_jwt import MyJWT
from app.accounts.models import User
from app.chats.models import Chat, Message
from app.common import db, mail, jwt, socketio

from app.chats import chats


@socketio.on('connect')
def test_connect():
    emit("event", "TEST")


@socketio.on('disconnect')
def test_disconnect():
    pass


@socketio.on('event')
@MyJWT.jwt_required()
def message(msg):
    pass


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
            user1 = User(username="root41", name="Vladislav", email="heamongus@mail.ru", password="Root_41")
            user2 = User(username="user41", name="FirstUser", email="user1@mail.ru", password="Root_41")

            # db.session.add(user1)
            # db.session.add(user2)
            # db.session.commit()

            user1 = User.query.filter_by(username='root41').first()
            user2 = User.query.filter_by(username='user41').first()

            # chat1 = Chat(id=1, title='First', users_in_chat=[user1, user2])
            # chat2 = Chat(id=2, title='Second', users_in_chat=[user2])
            # chat3 = Chat(id=3, title='Third', users_in_chat=[user1])
            # chat4 = Chat(id=4, title='Forth', users_in_chat=[user1])

            chat2 = User.query.filter_by(id=2).first()

            msg5_text = "Say in Second chat a very big message Say in Second chat a very big message Say in Second " \
                        "chat a very big message Say in Second chat a very big message Say in Second chat a very big " \
                        "message Say in Second chat a very big message Say in Second chat a very big message "
            # msg1 = Message(id=1, text="root41 say in First chat", user_username=user1.username, chat_id=chat1.id)
            # msg2 = Message(id=2, text="root41 say in Second chat", user_username=user1.username, chat_id=chat2.id)
            # msg3 = Message(id=3, text="user41 say in First chat", user_username=user2.username, chat_id=chat1.id)
            # msg4 = Message(id=4, text="user41 say in Second chat", user_username=user2.username, chat_id=chat2.id)
            # msg5 = Message(id=5, text=msg5_text, user_username=user2.username, chat_id=chat2.id)

            # db.session.add(chat1)
            # db.session.add(chat2)
            # db.session.add(chat3)
            # db.session.add(chat4)
            # db.session.add(msg1)
            # db.session.add(msg2)
            # db.session.add(msg3)
            # db.session.add(msg4)
            # db.session.add(msg5)
            #
            # db.session.commit()

            print(User.query.all())
            print(Chat.query.all())

            print(f'User1 msgs:{user1.messages.all()}')
            print(f'User2 msgs:{user2.messages.all()}')

            chat1 = Chat.query.filter_by(title='First').first()
            chat2 = Chat.query.filter_by(title='Second').first()
            print(f'Chats\n {chat1.users_in_chat}\n {chat2.users_in_chat}')

            print(user1.chats.all())
        except Exception as e:
            print(e)

    return socketio, app




