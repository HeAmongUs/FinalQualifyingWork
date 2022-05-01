from flask import Blueprint


chats = Blueprint('accounts', __name__,)


@chats.route("/chats")
def chats():
    pass
