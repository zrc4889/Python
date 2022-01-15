import json
import threading
from socket import *
from time import ctime


class PyChattingServer:
    __socket = socket(AF_INET, SOCK_STREAM, 0)
    __address = ('', 12231)

    __buf = 1024

    def __init__(self):
        self.__socket.bind(self.__address)
        self.__socket.listen(20)
        self.__msg_handler = ChattingHandler()

    def start_session(self):
        print('等待客户连接...\r\n')
        try:
            while True:
                cs, caddr = self.__socket.accept()
                # 利用handler来管理线程,实现线程之间的socket的相互通信
                self.__msg_handler.start_thread(cs, caddr)
        except socket.error:
            pass


class ChattingThread(threading.Thread):
    __buf = 1024

    def __init__(self, cs, caddr, msg_handler):
        super(ChattingThread, self).__init__()
        self.__cs = cs
        self.__caddr = caddr
        self.__msg_handler = msg_handler

    # 使用多线程管理会话
    def run(self):
        try:
            print('...连接来自于:', self.__caddr)
            data = '欢迎你到来kenwanmao聊天室！请输入你的的昵称（不能带空格）：'
            self.__cs.sendall(bytes(data, 'utf-8'))
            while True:
                data = self.__cs.recv(self.__buf).decode('utf-8')
                if not data:
                    break
                self.__msg_handler.handle_msg(data, self.__cs)
                print(data)
        except socket.error as e:
            print(e.args)
            pass
        finally:
            self.__msg_handler.close_conn(self.__cs)
            self.__cs.close()


class ChattingHandler:
    __help_str = "[ SYSTEM ]\r\n" \
                 "输入/checkol,即可获得所有登陆用户信息\r\n" \
                 "输入/h,即可获得帮助\r\n" \
                 "输入@用户名 (注意用户名后面的空格)+消息,即可发动单聊\r\n" \
                 "输入/i,即可屏蔽群聊信息\r\n" \
                 "再次输入/i,即可取消屏蔽\r\n" \
                 "所有首字符为/的信息都不会发送出去"

    __buf = 1024
    __socket_list = []

    __user_name_to_socket = {}
    __socket_to_user_name = {}

    __user_name_to_broadcast_state = {}

    def start_thread(self, cs, caddr):
        self.__socket_list.append(cs)
        chat_thread = ChattingThread(cs, caddr, self)
        chat_thread.start()

    def close_conn(self, cs):
        if cs not in self.__socket_list:
            return
        # 去除socket的记录
        nickname = "SOMEONE"
        if cs in self.__socket_list:
            self.__socket_list.remove(cs)
        # 去除socket与username之间的映射关系
        if cs in self.__socket_to_user_name:
            nickname = self.__socket_to_user_name[cs]
            self.__user_name_to_socket.pop(self.__socket_to_user_name[cs])
            self.__socket_to_user_name.pop(cs)
            self.__user_name_to_broadcast_state.pop(nickname)
        nickname += " "
        # 广播某玩家退出聊天室
        self.broadcast_system_msg(nickname + "离开了本聊天室")

    # 管理用户输入的信息
    def handle_msg(self, msg, cs):
        js = json.loads(msg)
        if js['type'] == "login":
            if js['msg'] not in self.__user_name_to_socket:
                if ' ' in js['msg']:
                    self.send_to(json.dumps({
                        'type': 'login',
                        'success': False,
                        'msg': '账号不能够带有空格'
                    }), cs)
                else:
                    self.__user_name_to_socket[js['msg']] = cs
                    self.__socket_to_user_name[cs] = js['msg']
                    self.__user_name_to_broadcast_state[js['msg']] = True
                    self.send_to(json.dumps({
                        'type': 'login',
                        'success': True,
                        'msg': '昵称建立成功,输入/checkol可查看所有在线的人,输入/help可以查看帮助(所有首字符为/的消息都不会发送)'
                    }), cs)
                    # 广播其他人,他已经进入聊天室
                    self.broadcast_system_msg(js['msg'] + "已经进入了聊天室")
            else:
                self.send_to(json.dumps({
                    'type': 'login',
                    'success': False,
                    'msg': '账号已存在'
                }), cs)
        # 若玩家处于屏蔽模式,则无法发送群聊消息
        elif js['type'] == "broadcast":
            if self.__user_name_to_broadcast_state[self.__socket_to_user_name[cs]]:
                self.broadcast(js['msg'], cs)
            else:
                self.send_to(json.dumps({
                    'type': 'broadcast',
                    'msg': '屏蔽模式下无法发送群聊信息'
                }), cs)
        elif js['type'] == "ls":
            self.send_to(json.dumps({
                'type': 'ls',
                'msg': self.get_all_login_user_info()
            }), cs)
        elif js['type'] == "help":
            self.send_to(json.dumps({
                'type': 'help',
                'msg': self.__help_str
            }), cs)
        elif js['type'] == "sendto":
            self.single_chatting(cs, js['nickname'], js['msg'])
        elif js['type'] == "ignore":
            self.exchange_ignore_state(cs)

    def exchange_ignore_state(self, cs):
        if cs in self.__socket_to_user_name:
            state = self.__user_name_to_broadcast_state[self.__socket_to_user_name[cs]]
            if state:
                state = False
            else:
                state = True
            self.__user_name_to_broadcast_state.pop(self.__socket_to_user_name[cs])
            self.__user_name_to_broadcast_state[self.__socket_to_user_name[cs]] = state
            if self.__user_name_to_broadcast_state[self.__socket_to_user_name[cs]]:
                msg = "通常模式"
            else:
                msg = "屏蔽模式"
            self.send_to(json.dumps({
                'type': 'ignore',
                'success': True,
                'msg': '[TIME : %s]\r\n[ SYSTEM ] : %s\r\n' % (ctime(), "模式切换成功,现在是" + msg)
            }), cs)
        else:
            self.send_to({
                'type': 'ignore',
                'success': False,
                'msg': '切换失败'
            }, cs)

    def single_chatting(self, cs, nickname, msg):
        if nickname in self.__user_name_to_socket:
            msg = '[TIME : %s]\r\n[ %s CHATTING TO %s ] : %s\r\n' % (
                ctime(), self.__socket_to_user_name[cs], nickname, msg)
            self.send_to_list(json.dumps({
                'type': 'single',
                'msg': msg
            }), self.__user_name_to_socket[nickname], cs)
        else:
            self.send_to(json.dumps({
                'type': 'single',
                'msg': '该用户不存在'
            }), cs)
        print(nickname)

    def send_to_list(self, msg, *cs):
        for i in range(len(cs)):
            self.send_to(msg, cs[i])

    def get_all_login_user_info(self):
        login_list = "[ SYSTEM ] ALIVE USER : "
        for key in self.__socket_to_user_name:
            login_list += self.__socket_to_user_name[key] + ",\r\n"
        return login_list

    def send_to(self, msg, cs):
        if cs not in self.__socket_list:
            self.__socket_list.append(cs)
        cs.sendall(bytes(msg, 'utf-8'))

    def broadcast_system_msg(self, msg):
        data = '[TIME : %s]\r\n[ SYSTEM ] : %s' % (ctime(), msg)
        js = json.dumps({
            'type': 'system_msg',
            'msg': data
        })
        # 屏蔽了群聊的玩家也可以获得系统的群发信息
        for i in range(len(self.__socket_list)):
            if self.__socket_list[i] in self.__socket_to_user_name:
                self.__socket_list[i].sendall(bytes(js, 'utf-8'))

    def broadcast(self, msg, cs):
        data = '[TIME : %s]\r\n[%s] : %s\r\n' % (ctime(), self.__socket_to_user_name[cs], msg)
        js = json.dumps({
            'type': 'broadcast',
            'msg': data
        })
        # 没有的登陆的玩家无法得知消息,屏蔽了群聊的玩家也没办法获取信息
        for i in range(len(self.__socket_list)):
            if self.__socket_list[i] in self.__socket_to_user_name \
                    and self.__user_name_to_broadcast_state[self.__socket_to_user_name[self.__socket_list[i]]]:
                self.__socket_list[i].sendall(bytes(js, 'utf-8'))


def main():
    server = PyChattingServer()
    server.start_session()


main()
