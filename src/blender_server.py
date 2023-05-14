import bpy
import struct
import socket
import numpy as np

def handle_command(command):
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
        vertex_data = np.array([vertex.co[:] for vertex in cube.data.vertices])
        face_data = np.array([polygon.vertices[:] for polygon in cube.data.polygons])

        # Convert the data to binary
        binary_vertex_data = vertex_data.astype('float32').tobytes()
        binary_face_data = face_data.astype('int32').tobytes()

        # Combine the vertex and face data
        binary_data = struct.pack('ii', len(vertex_data), len(face_data)) + binary_vertex_data + binary_face_data

        return binary_data

    return b'Invalid command'

def run_socket_server():
    print("Socket server listening on localhost:5001")
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
                    conn.sendall(response)

run_socket_server()
