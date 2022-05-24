from flask import request, make_response, jsonify

from .models import Chat
from ..accounts import MyJWT
from ..common import socketio, db
from app.chats import chats


@chats.route("/list", methods=['GET'])
@MyJWT.jwt_required()
def get_chats():
    user_chats = MyJWT.get_current_user().chats.all()
    return jsonify([chat.serialize for chat in user_chats])


@chats.route("/<chat_id>/messages", methods=['GET'])
@MyJWT.jwt_required()
def get_messages(chat_id):
    chat = Chat.query.filter_by(id=chat_id).first()
    if MyJWT.get_current_user() in chat.users_in_chat:
        # Если пользователь имеет доступ в чат
        chat_messages = chat.messages
        return jsonify([msg.serialize for msg in chat_messages])
    return make_response(404)


# СОКЕТЫ не работает все что ниже
@chats.route("/<chat_id>/enter", methods=['POST'])
@MyJWT.jwt_required()
def enter_in_chat(chat_id: int):
    if chat_id:
        chat = Chat.query.filter_by(id=chat_id).first()
        current_user = MyJWT.get_current_user()
        chat.users_in_chat.append(current_user)
        db.session.comit()


# SOCKET
@chats.route("/<chat_id>/leave", methods=['ВУДУЕУ'])
@MyJWT.jwt_required()
def leave_from_chat():
    # получтиь пользователя
    # удалить из чата из запроса
    pass


@socketio.on('connect')
@MyJWT.jwt_required()
def send_message(chat_id):
    current_user = MyJWT.get_current_user()
    # получтиь пользователя
    # получить чат из запроса
    # добавить сообщение в чат
    pass
