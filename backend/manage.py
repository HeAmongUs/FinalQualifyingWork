from app import create_app


socketio, current_app = create_app()
app = socketio

if __name__ == '__main__':
    socketio.run(current_app, port=8000,)
