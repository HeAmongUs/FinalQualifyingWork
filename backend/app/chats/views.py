from flask import jsonify
from flask_socketio import emit

from .models import Chat, Message
from ..accounts import MyJWT
from ..common import socketio, db
from app.chats import chats


@chats.route("/list", methods=['GET'])
@MyJWT.jwt_required()
def get_chats():
    user_chats = MyJWT.get_current_user().chats.all()
    return jsonify([chat.serialize for chat in user_chats])


@chats.route("/list/<title>", methods=['GET'])
@MyJWT.jwt_required()
def get_searched_chats(title):
    searched_chats = Chat.query.filter(Chat.title.contains(title)).all()
    return jsonify([chat.serialize for chat in searched_chats])


@chats.route("/<chat_id>/messages", methods=['GET'])
@MyJWT.jwt_required()
def get_messages(chat_id):
    chat = Chat.query.filter_by(id=chat_id).first()
    if MyJWT.get_current_user() in chat.users_in_chat:
        return jsonify([msg.serialize for msg in chat.messages])
    return jsonify({})


# СОКЕТЫ
# не работает все что ниже
@chats.route("/<chat_id>/enter", methods=['POST'])
@MyJWT.jwt_required()
def enter_in_chat(chat_id: int):
    if chat_id:
        chat = Chat.query.filter_by(id=chat_id).first()
        current_user = MyJWT.get_current_user()
        chat.users_in_chat.append(current_user)
        db.session.comit()


# SOCKET
@chats.route("/<chat_id>/leave", methods=['DELETE'])
@MyJWT.jwt_required()
def leave_from_chat(chat_id):
    if chat_id:
        chat = Chat.query.filter_by(id=chat_id).first()
        current_user = MyJWT.get_current_user()
        chat.users_in_chat.remove(current_user)
        db.session.comit()


@socketio.on("send message")
@MyJWT.jwt_required()
def send_message(payload):
    chat_id = payload.get("chatId")
    current_user = MyJWT.get_current_user()
    chat = Chat.query.filter_by(id=chat_id).first()
    if current_user in chat.users_in_chat:
        text = payload.get("messageText")
        new_msg = Message(text=text, user_username=current_user.username, chat_id=chat_id)
        db.session.add(new_msg)
        db.session.commit()
        new_msg = Message.query.filter_by(chat_id=chat_id, user_username=current_user.username, text=text).first()
        print(new_msg)
        emit("display new message", new_msg.serialize, broadcast=True)
