import socket
import win32com.client 

# 预装了屏蔽词的朗读

speak = win32com.client.Dispatch('SAPI.SPVOICE')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    host = input("Host:")
    s.connect((host,1234)) # 仅可使用1234端口
    while True:
        msg = input("Send:")
        s.sendall(msg.encode('utf-8'))
        data = s.recv(1024)
        print("Received:",data.decode('utf-8'))
        speak.Speak(data.decode('utf-8'))