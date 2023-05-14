import bpy
import socket
import struct
import numpy as np
from queue import Queue
from threading import Thread

command_queue = Queue()
    

def process_commands():
    while True:
        if not command_queue.empty():
            conn, command = command_queue.get()
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

                # Pack the number of vertices and faces as int32
                binary_data = struct.pack('ii', len(vertex_data), len(face_data)) + binary_vertex_data + binary_face_data

                # Send the binary data over the socket
                conn.sendall(binary_data)

            command_queue.task_done()


def run_socket_server():
    print("Socket server listening on localhost:5001")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('localhost', 5001))
        s.listen()
        try:
            while True:
                conn, addr = s.accept()
                with conn:
                    print('Connected by', addr)
                    while True:
                        data = conn.recv(1024)
                        if not data:
                            break
                        command = data.decode('utf-8')
                        command_queue.put((conn, command))

        except KeyboardInterrupt:
            print("Socket server killed ...")

# Start the socket server in a separate thread
socket_server = Thread(target=run_socket_server)
socket_server.start()

print("Processing queue ...")
process_commands()