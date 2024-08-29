import socket
import cv2
import pickle
import struct
import threading
import sounddevice as sd
import numpy as np

class VideoClient:
    def __init__(self, server_ip, username):
        self.server_ip = server_ip
        self.server_port = 9999
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.username = username
        self.connection_established = False

    def receive_video(self):
        try:
            self.client_socket.connect((self.server_ip, self.server_port))
            self.connection_established = True
            data = b""
            payload_size = struct.calcsize("Q")
            while True:
                while len(data) < payload_size:
                    packet = self.client_socket.recv(4*1024)
                    if not packet:
                        break
                    data += packet
                packed_msg_size = data[:payload_size]
                data = data[payload_size:]
                msg_size = struct.unpack("Q", packed_msg_size)[0]
                while len(data) < msg_size:
                    data += self.client_socket.recv(4*1024)
                frame_data = data[:msg_size]
                data = data[msg_size:]
                frame = pickle.loads(frame_data)
                cv2.imshow("Received", frame)
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
        except Exception as e:
            print("Error:", e)
        finally:
            self.client_socket.close()
            cv2.destroyAllWindows()

    def receive_audio(self):
        def audio_callback(outdata, frames, time, status):
            try:
                audio_data = self.client_socket.recv(4096)
                outdata[:] = np.frombuffer(audio_data, dtype=np.float32).reshape((frames, 2))
            except Exception as e:
                print("Error receiving audio:", e)

        with sd.OutputStream(callback=audio_callback):
            sd.sleep(100000)

    def send_message(self, message):
        if self.connection_established:
            try:
                full_message = f"{self.username}: {message}"
                self.client_socket.sendall(full_message.encode())
            except Exception as e:
                print("Error while sending message:", e)

def start_client():
    server_ip = input("Enter the server IP address: ")
    username = input("Enter your username: ")
    client = VideoClient(server_ip, username)
    video_thread = threading.Thread(target=client.receive_video)
    audio_thread = threading.Thread(target=client.receive_audio)
    video_thread.start()
    audio_thread.start()
    while True:
        message = input(f"{username}: ")
        client.send_message(message)

if __name__ == "__main__":
    start_client()
