import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    host = input("host:")
    s.connect((host,1234)) # 仅可使用1234端口
    while True:
        msg = input("Send:")
        s.sendall(msg.encode('utf-8'))
        data = s.recv(1024)
        print("Received:",data.decode('utf-8'))