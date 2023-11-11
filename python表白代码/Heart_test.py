import random
import tkinter as tk
from math import sin,cos,pi
import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":
    root = tk.Tk()
    canvas = tk.Canvas(root,width="640",height="640")
    canvas.pack()

    '''
    #验证Heart的heart_function的功能，确实能产生一个心形，只不过是倒着的
    t1=[]
    for _ in range(2000):
        t=random.uniform(0,2*pi)
        t1.append(t)
    x1,y1=[],[]


    #用np.linspace得到的图形更具体，一个空心的倒心形
    # t1 = np.linspace(0, 2 * pi, 2000)
    for i in t1:
        x = 16 * (sin(i) ** 3)
        y = -(13 * cos(i) - 5 * cos(2 * i) - 2 * cos(3 * i) - cos(4 * i))
        x *= 11  # x=x*11 x按比例扩大
        y *= 11  # y=y*11 y按比例扩大
        x += 320  # 水平方向从中心向外辐射
        y += 320  # 竖直方向从中心向外辐射
        x1.append(x)
        y1.append(y)
    
    plt.plot(x1,y1)  #该不该用plt还不知道
    plt.show()
    
    '''
