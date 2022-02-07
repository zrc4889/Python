import socket
import threading


def handle_client(c, addr):

    print(addr, "connected.")
    dirt = 0
    while True:
        data = c.recv(1024)
        if not data:
            break
        f1 = ["迷你", "mini",
              "MD", "cmn",
              "TMD", "他妈的",
              "马牛逼", "丁三石",
              "吊", "蛋蛋",
              "鸡鸡", "草",
              "智障", "NB",
              "牛逼", "大便",
              "屎", "尿",
              "你妈", "囸",
              "SB", "VIP",
              "vip", "MMP",
              "mmp", "屁",
              "仙人", "先人",
              "妈逼", "fuck",
              "FUCK", "Fuck",
              "王八蛋", "你奶奶的",
              "你妈死了", "逼",
              "傻逼", "煞笔",
              "沙比", "沙壁",
              "nmsl", "sb",
              "马化腾", "麻花疼",
              "丁三石", "作弊",
              "脑子有病", "操",
              "卧槽", "我操",
              "握草", "特么的",
              "你妈的", "妈蛋",
              "装逼", "nm",
              "jb", "操",
              "傻", "猪",
              "变态", "死",
              "歹"]
        speak = data.decode('utf-8')
        d = {'*'}
        for i in f1:
            speak = speak.replace(i, '*')
        for d in speak:
            dirt = dirt+1
        print(speak)
        print((addr), " says:", speak)
        if dirt >= 3:
            c.sendall(
                'You are banned from this server, try again.'.encode('utf-8'))
            return 
        else:
            c.sendall(speak.encode('utf-8'))  # 重复发送消息
            print(dirt)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(("127.0.0.1", 1234))
    s.listen(5)

    while True:
        c, addr = s.accept()

        t = threading.Thread(target=handle_client, args=(c, addr))
        t.start()
