import socket
while True:
    address = ('127.0.0.1', 5005)  # 服务端地址和端口
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(address)  # 绑定服务端地址和端口
    s.listen(5)
    conn, addr = s.accept()  # 返回客户端地址和一个新的 socket 连接
    print('[+] Connected with', addr)
    while True:
        try:
            data = conn.recv(1024)  # buffersize 等于 1024
            data = data.decode()
            if not data:
                break
            if data == "fuck":
                conn.close()
            else:
                print(data)
        except:
            conn.close()
    s.close()
