import socket
import cv2
import pickle
import struct
import threading

class ClientHandler(threading.Thread):
    def __init__(self, client_socket, addr):
        super().__init__()
        self.client_socket = client_socket
        self.addr = addr

    def run(self):
        print('GOT CONNECTION FROM:', self.addr)
        vid = cv2.VideoCapture(0)

        while vid.isOpened():
            ret, frame = vid.read()
            if not ret:
                break

            # Serialize the frame
            data = pickle.dumps(frame)
            message = struct.pack("Q", len(data)) + data

            # Send the frame to the client
            try:
                self.client_socket.sendall(message)
            except:
                print("Connection closed by client.")
                break

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break

        # Release resources
        self.client_socket.close()
        vid.release()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
print("host name", host_name)
host_ip = socket.gethostbyname(host_name)
print('HOST IP:', host_ip)
port = 9999
socket_address = (host_ip, port)
server_socket.bind(socket_address)
server_socket.listen(5)
print("LISTENING AT:", socket_address)

while True:
    client_socket, addr = server_socket.accept()
    handler = ClientHandler(client_socket, addr)
    handler.start()
