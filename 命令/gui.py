#!/usr/bin/python
from tkinter import *
import os

# 此项目已改变内核并独立至 TimeClickGO

root=Tk()
 
def Show():
    if En.get()=='exit':
      root.quit()
    if En.get()=="web":
      os.system("start http://cn.bing.com")
    if En.get()=="luogu":
      os.system("start http://www.luogu.com.cn")

root.geometry("175x30")
root.minsize(width=175,height=30)
root.maxsize(width=175,height=30)

En=Entry(root)
En.grid(row=1,column=0)
Button(root,text='run',width=3,height=1,command=Show).grid(row=1,column=1)

root.mainloop()