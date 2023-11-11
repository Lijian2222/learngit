import tkinter as tk
import random
import threading
import time


def dow():
    window = tk.Tk()
    width = window.winfo_screenwidth()
    height = window.winfo_screenheight()
    a = random.randrange(0, width)
    b = random.randrange(0, height)
    window.title('祝赵婉莹立冬快乐')  # 弹窗的名字，都可以修改的
    window.geometry("250x50" + "+" + str(a) + "+" + str(b))  # 弹窗大小，不建议修改
    tk.Label(window,
             text='祝赵婉莹立冬快乐！',  # 标签的文字，随便改
             bg='Red',  # 背景颜色
             font=('楷体', 17),  # 字体和字体大小
             width=20, height=2  # 标签长宽
             ).pack()  # 固定窗口位置
    window.mainloop()


threads = []
for i in range(100):  # 需要的弹框数量，别太多了，电脑不好的话怕你死机
    t = threading.Thread(target=dow)
    threads.append(t)
    time.sleep(0.1)
    threads[i].start()
