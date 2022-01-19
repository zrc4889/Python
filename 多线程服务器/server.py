import socket
import threading

def handle_client(c, addr):
    print(addr, "connected.")

    while True:
        data = c.recv(1024)
        if not data:
            break
        print((addr)," says:",data.decode('utf-8'))
        c.sendall(data) # 重复发送消息

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(("192.168.6.247", 1234))
    s.listen(5)

    while True:
        c, addr = s.accept()

        t = threading.Thread(target=handle_client, args=(c, addr))
        t.start()