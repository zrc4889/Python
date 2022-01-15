from http import client
import socket
import sys

# 创建对象
serversocket = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM)

# 获取本地的网络信息
host = socket.gethostname()
port = 9999

# 绑定
serversocket.bind((host,port))

# 最大连接数
serversocket.listen(5)

while True:
    clientsocket,addr = serversocket.accept()
    # 同意连接，记下客户端地址

    print("连接地址: %s" % str(addr))

    msg = '欢迎访问!' + "\r\n"
    clientsocket.send(msg.encode('utf-8')) # 设置编码
    clientsocket.close()
