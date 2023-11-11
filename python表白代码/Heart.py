import random
from math import sin,cos,pi,log
from tkinter import *



CANVAS_WIDTH = 640
CANVAS_HEIGHT = 480
CANVAS_CENTER_X = CANVAS_WIDTH/2
CANVAS_CENTER_Y = CANVAS_HEIGHT/2
IMAGE_ENLARGE = 11
HEART_COLOR = "#ff2121"  #00ffff #FFC0CB #FFFF99 #0000FF

def heart_function(t,shrink_ratio:float = IMAGE_ENLARGE):#用于计算爱心的坐标点
    #t是0到2*pi之间的随机数
    x = 16*(sin(t)**3)
    y = -(13*cos(t)-5*cos(2*t)-2*cos(3*t)-cos(4*t))

    x*=shrink_ratio #x=x*11 x按比例扩大
    y*=shrink_ratio #y=y*11 y按比例扩大

    x+=CANVAS_CENTER_X #水平方向从中心向外辐射
    y+=CANVAS_CENTER_Y #竖直方向从中心向外辐射

    return int(x),int(y)

def scatter_inside(x,y,beta=0.15): #用于在爱心的边缘上扩散点的坐标
    ratio_x=-beta*log(random.random())
    ratio_y=-beta*log(random.random())

    dx = ratio_x *(x - CANVAS_CENTER_X)
    dy = ratio_y * (y - CANVAS_CENTER_Y)

    return x - dx, y - dy

def shrink(x,y,ratio): #用于缩放点的坐标
    force = -1 / (((x - CANVAS_CENTER_X) ** 2 + (y - CANVAS_CENTER_Y) **2)** 0.6)  # 这个参数..
    dx = ratio * force * (x - CANVAS_CENTER_X)
    dy = ratio * force * (y - CANVAS_CENTER_Y)
    return x - dx,y - dy

def curve(p): #用于生成一个平滑的周期函数
    return 2 * (2 * sin(4 * p)) / (2 * pi)


class Heart: #用于构建和绘制爱心
    def __init__(self, generate_frame=20):
        self._points = set()  # 原始爱心坐标集合
        self._edge_diffusion_points = set()  # 边缘扩散效果点坐标集合
        self._center_diffusion_points = set()  # 中心扩散效果点坐标集合
        self.all_points = {} # 每动态点坐标

        self.build(2000) #产生2000个点并加入到_point里面

        self.random_halo = 1000

        self.generate_frame = generate_frame #20
        for frame in range(generate_frame): #重复20次calc函数
            self.calc(frame)

    def build(self, number): #用于构建爱心的原始坐标集合和边缘扩散效果点集合
        for _ in range(number):
            t = random.uniform(0,2 * pi)
            x,y = heart_function(t)
            self._points.add((x, y))

        for _x, _y in list(self._points):
            for _ in range(3):
                x,y = scatter_inside(_x,_y,0.05)
                self._edge_diffusion_points.add((x,y))

    def calc_position(self,x,y,ratio): # 用于计算动态点的新位置和大小，并将其添加到all_points字典中
        force = 1 / (((x - CANVAS_CENTER_X) ** 2 + (y - CANVAS_CENTER_Y) ** 2) ** 0.520) # 魔法参数
        dx = ratio * force * (x - CANVAS_CENTER_X) + random.randint(-1,1)
        dy = ratio * force * (y - CANVAS_CENTER_Y) + random.randint(-1,1)
        return x - dx, y - dy

    def calc(self,generate_frame): #用于计算每个动态点的位置和大小，并将其添加到all_points字典中
        ratio = 10 * curve(generate_frame / 10 * pi)
        # 圆滑的周期的缩放比例
        halo_radius = int(4 + 6 * (1 + curve(generate_frame / 10 * pi)))
        halo_number = int(3000 + 4000 * abs(curve(generate_frame / 10 * pi) ** 2))

        all_points = []   # 重新声明了一个数组？
        heart_halo_point = set()

        for _ in range(halo_number):
            t = random.uniform(0,2 * pi)
            x,y = heart_function(t, shrink_ratio=11.6)
            x,y = shrink(x,y, halo_radius)
            if (x, y) not in heart_halo_point:
                heart_halo_point.add((x,y))
                x += random.randint(-14,14)
                y += random.randint(-14,14)
                size = random.choice((1,2,2))
                all_points.append((x, y,size))

        for x, y in self._points: #原始坐标点
            x,y = self.calc_position(x,y, ratio)
            size = random.randint(1,3) #1或者2
            all_points.append((x,y,size))

        for x,y in self._edge_diffusion_points:
            x,y = self.calc_position(x, y, ratio)
            size = random.randint(1, 2)
            all_points.append((x, y, size))

        for x,y in self._center_diffusion_points:
            x,y = self.calc_position(x,y, ratio)
            size = random.randint(1,2)
            all_points.append((x,y, size))

        self.all_points[generate_frame] = all_points

    def render(self, render_canvas, render_frame): #用于绘制爱心的图形
        for x, y, size in self.all_points[render_frame % self.generate_frame]:
            render_canvas.create_rectangle(x,y,x + size,y + size,width=0, fill=HEART_COLOR)

#draw函数用于绘制爱心图形，并使用Tkinter的Canvas和Heart类进行实现
def draw(main: Tk, render_canvas: Canvas, render_heart:Heart, render_frame=0):
        render_canvas.delete('all') # cavas删除"all"?
        render_heart.render(render_canvas, render_frame)
        #160ms后调用draw函数一次
        main.after(160, draw, main, render_canvas, render_heart,render_frame + 1)

if __name__=="__main__":
     root = Tk()  # 一个Tk
     canvas = Canvas(root,bg = 'black',height = CANVAS_HEIGHT,width=CANVAS_WIDTH)
     canvas.pack()

     heart = Heart()
     draw(root, canvas, heart)

     root.mainloop()

