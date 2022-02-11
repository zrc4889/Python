import threading
import tkinter
from tkinter.messagebox import askretrycancel
from ttkbootstrap import Style
from tkinter import ttk
from tkinter.messagebox import *
import os
import time


def t():
    time_left = 1200
    while time_left > 0:
        # print('倒计时(s):', time_left)
        time.sleep(1)
        time_left = time_left - 1
    tkinter.messagebox.showwarning('警告','20分钟使用时间已结束，请保存工作并立刻离开此电脑休息。')
    os.system("logoff")


def open_mode():
    getch = tkinter.messagebox.askyesno('提示', '要结束qq、微信并打开洛谷吗？（时间：20分钟）')
    if getch == False:
        return
    # 目前效果：终止qq，微信。打开洛谷相关页面
    os.system("start https://www.luogu.com.cn")
    os.system("start https://www.luogu.com.cn/problem/list")
    os.system("taskkill /f /t /im qq.exe")
    os.system("taskkill /f /t /im WeChat.exe")
    t1 = threading.Thread(target=t)
    t1.start()


def shutdown():
    os.system("logoff")


style = Style(theme='lumen')
window = style.master
# window = tkinter.tk()
ttk.Button(window, text="Open Mode", command=open_mode, style='success.TButton').pack(
    side='left', padx=5, pady=10)
ttk.Button(window, text="Log off", command=shutdown, style='success.Outline.TButton').pack(
    side='left', padx=5, pady=10)
window.mainloop()
