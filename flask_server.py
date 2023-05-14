from flask import Flask, request, jsonify
import socket
import json

app = Flask(__name__)

@app.route('/data', methods=['POST'])
def get_data():
    command = request.json.get('command')

    if command == 'cube':
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(('localhost', 5001))
            s.sendall(command.encode('utf-8'))
            data = s.recv(1024)
        response = json.loads(data.decode('utf-8'))
        if 'error' in response:
            return jsonify(error=response['error']), 400
        return jsonify(vertices=response['vertices'], faces=response['faces'])

    return jsonify(error='Invalid command'), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
