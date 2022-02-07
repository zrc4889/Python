class Box:
    def __init__(self, w, h, l):  # __init__函数自动执行
        self.w = w  # self 指代自己
        self.h = h
        self.l = l

    def volume(self):
        print(self.w*self.h*self.l)
