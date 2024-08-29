import socket

host ='127.0.0.1'
port =9999

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host,port))
    message = input ("Enter the text in lower case:")
    s.sendall(message.encode())
    data = s.recv(1024)
    print("From the server: ",data.decode()) 
s.close()
