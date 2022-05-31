from app import create_app


socketio, current_app = create_app()
app = socketio

if __name__ == '__main__':
    socketio.run(current_app, host="192.168.43.108", port=8000)
