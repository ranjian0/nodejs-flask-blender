import bpy
import json
import socket

def handle_command(command):
    print(command, command == 'cube')
    if command == 'cube':
        # Delete all mesh objects
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.select_by_type(type='MESH')
        bpy.ops.object.delete()

        # Create a new cube
        bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, location=(0, 0, 0))

        # Get the created cube
        cube = bpy.context.selected_objects[0]

        # Get the vertex and face data
        vertex_data = [vertex.co[:] for vertex in cube.data.vertices]
        face_data = [polygon.vertices[:] for polygon in cube.data.polygons]

        return json.dumps({'vertices': vertex_data, 'faces': face_data})

    return json.dumps({'error': 'Invalid command'})

def run_socket_server():
    print("Running socket server at localhost:5001")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('localhost', 5001))
        s.listen()
        while True:
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    response = handle_command(data.decode('utf-8'))
                    conn.sendall(response.encode('utf-8'))

run_socket_server()
