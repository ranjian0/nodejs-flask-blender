from flask import Flask, request, Response
import socket

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    return "Hello"

@app.route('/data', methods=['POST'])
def get_data():
    command = request.json.get('command')

    if command == 'cube':
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(('localhost', 5001))
            s.sendall(command.encode('utf-8'))
            data = s.recv(1024)
        return Response(data, mimetype='application/octet-stream')

    return Response(b'Invalid command', status=400)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
