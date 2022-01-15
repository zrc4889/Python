import json
import threading
from socket import *

is_login = False
is_broadcast = True

#接受消息类
class ClientReceiveThread(threading.Thread):
    __buf = 1024
    #初始化
    def __init__(self, cs):
        super(ClientReceiveThread, self).__init__()
        self.__cs = cs
    def run(self):
        self.receive_msg()

    def receive_msg(self):
        while True:
            msg = self.__cs.recv(self.__buf).decode('utf-8')
            if not msg:
                break
            js = json.loads(msg)
            if js['type'] == "login":
                if js['success']:
                    global is_login
                    is_login = True
                print(js['msg'])
            elif js['type'] == "ignore":
                if js['success']:
                    global is_broadcast
                    if is_broadcast:
                        is_broadcast = False
                    else:
                        is_broadcast = True
                print(js['msg'])
            else:
                if not is_broadcast:
                    print("[现在处于屏蔽模式]")
                print(js['msg'])

#发送消息类
class ClientSendMsgThread(threading.Thread):

    def __init__(self, cs):
        super(ClientSendMsgThread, self).__init__()
        self.__cs = cs
    def run(self):
        self.send_msg()

    # 根据不同的输入格式来进行不同的聊天方式
    def send_msg(self):
        while True:
            js = None
            msg = input()
            if not is_login:
                js = json.dumps({
                    'type': 'login',
                    'msg': msg
                })
            #包含@，表示进入私聊模式
            elif msg[0] == "@":
                data = msg.split(' ')
                if not data:
                    print("请重新输入")
                    break
                nickname = data[0]
                nickname = nickname.strip("@")
                if len(data) == 1:
                    data.append(" ")
                js = json.dumps({
                    'type': 'sendto',
                    'nickname': nickname,
                    'msg': data[1]
                })
            elif msg == "/help":
                js = json.dumps({
                    'type': 'help',
                    'msg': None
                })
            elif msg == "/checkol":
                js = json.dumps({
                    'type': 'ls',
                    'msg': None
                })
            elif msg == "/i":
                js = json.dumps({
                    'type': 'ignore',
                    'msg': None
                })
            else:
                if msg[0] != '/':
                    js = json.dumps({
                        'type': 'broadcast',
                        'msg': msg
                    })
            if js is not None:
                self.__cs.sendall(bytes(js, 'utf-8'))

def main():
    buf = 1024
    # 改变这个的地址,变成服务器的地址,那么只要部署到服务器上就可以全网使用了
    address = ("127.0.0.1", 12231)
    cs = socket(AF_INET, SOCK_STREAM, 0)
    cs.connect(address)
    data = cs.recv(buf).decode("utf-8")
    if data:
        print(data)
    receive_thread = ClientReceiveThread(cs)
    receive_thread.start()
    send_thread = ClientSendMsgThread(cs)
    send_thread.start()
    while True:
        pass

main()
