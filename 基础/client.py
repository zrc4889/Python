import socket
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 获取本地主机名和端口号
host = socket.gethostname()

# 设置端口号
port = 9999

# 连接
s.connect((host,port))

# 限制数据大小
msg = s.recv(1024) 

s.close()

print (msg.decode('utf-8'))