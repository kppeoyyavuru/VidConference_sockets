import socket
import threading


HOST = '10.1.0.173'  
PORT = 65430


def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(message)
        except Exception as e:
            print(f"Error receiving message: {e}")
            break


def start_client():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((HOST, PORT))
            print("Connected to the server.")

            
            username = input("Enter your username: ")
            client_socket.sendall(username.encode('utf-8'))

            
            receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
            receive_thread.start()

            
            while True:
                message = input("Type your message: ")
                client_socket.sendall(message.encode('utf-8'))
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
  start_client()
#'C:\\Users\\eshit\\AppData\\Local\\Programs\\Python\\Python311\\Lib\\site-packages\\certifi\\cacert.pem'