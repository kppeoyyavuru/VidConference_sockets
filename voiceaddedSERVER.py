import socket
import cv2
import pickle
import struct
import threading
import sounddevice as sd
import numpy as np

class ClientHandler(threading.Thread):
    def __init__(self, client_socket, addr):
        super().__init__()
        self.client_socket = client_socket
        self.addr = addr

    def receive_video(self):
        vid = cv2.VideoCapture(0)
        while True:
            ret, frame = vid.read()
            if not ret:
                break
            data = pickle.dumps(frame)
            message = struct.pack("Q", len(data)) + data
            try:
                self.client_socket.sendall(message)
            except:
                print("Connection closed by client.")
                break
        vid.release()

    def receive_audio(self, indata, frames, time, status):
        message = indata.copy()
        message = message.tobytes()
        try:
            self.client_socket.sendall(message)
        except:
            print("Connection closed by client.")

    def run(self):
        print('GOT CONNECTION FROM:', self.addr)
        sd.default.samplerate = 44100
        sd.default.channels = 2
        with sd.InputStream(callback=self.receive_audio):
            self.receive_video()
            self.client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_name = socket.gethostname()
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

if __name__ == "__main__":
    start_server()
