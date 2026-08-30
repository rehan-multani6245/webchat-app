import os
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'change-this-secret-key'
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('join')
def handle_join(data):
    nickname = data.get('nickname', 'Someone')
    emit('message', {'nickname': 'System', 'text': f'{nickname} joined the chat'}, broadcast=True)

@socketio.on('send_message')
def handle_message(data):
    # data has 'nickname' and 'text'
    emit('message', data, broadcast=True)

if __name__ == '__main__':
    # host='0.0.0.0' makes it reachable from other devices on the network
    # PORT comes from the hosting service (like Render) when deployed online
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port, debug=False, allow_unsafe_werkzeug=True)
