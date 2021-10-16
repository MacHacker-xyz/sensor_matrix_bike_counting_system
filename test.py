import math
import numpy as np   

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.pylab import mpl
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
import tkinter as tk
import KM
import model
import random

 
mpl.rcParams['font.sans-serif'] = ['SimHei']  #中文显示
mpl.rcParams['axes.unicode_minus']=False      #负号显示



def circle(x,y,r,color='k',count=100):
    xarr=[]
    yarr=[]
    for i in range(count):
        j = float(i)/count * 2 * np.pi
        xarr.append(y+r*np.cos(j))
        yarr.append(x+r*np.sin(j))
    plt.plot(xarr,yarr,c=color)

def xuxian_circle(x,y,r,color='k',count=100):
    xarr=[]
    yarr=[]
    flag = False
    for i in range(count):
        if i%int(count/10)==int(count/20):
            flag = True
        elif i%int(count/10)<=int(count/20):
            j = i/count * 2 * np.pi
            xarr.append(y+r*np.cos(j))
            yarr.append(x+r*np.sin(j))
            flag = False
        elif i%int(count/5)>=int(count/20):
            xarr=[]
            yarr=[]
        if flag:
            plt.plot(xarr,yarr,c=color)


 
class From:
    def __init__(self,root,scale_x,scale_y,number): 
        matplotlib.use("Agg")
        self.root = root
        self.flag = True
        self.Canvas=None
        self.line=[(25,25),(0,50)]
        # 这里定义一下追踪器对象
        self.tracker = KM.Tracker(line=self.line)
        # 这里定义一下传感器阵列
        self.matrix = np.zeros((100,100))
        self.number = number
        self.figure = None
        while(True):
            #time.sleep(time_scale)
            self.matrix = np.zeros((50,50))
            x = int(50*scale_x.get()/500.0)
            y = int(50*scale_y.get()/500.0)
            x1 = x+2
            x2 = x-2
            points = [(y,x1),(y,x2)]
            value = 100
            dx = 0.1
            dy = 0.1
            # format the data:
            for point in points:
                (X,Y) = point
                if X>=0 and X<self.matrix.shape[0] and Y>=0 and Y<self.matrix.shape[1]:
                
                    if X>=3 and X<self.matrix.shape[0]-3 and Y>=3 and Y<self.matrix.shape[1]-3:
                        for i in range(10):
                            theta = 2*i*math.pi/10
                            self.matrix[int(X+0.3/dx*math.cos(theta)),int(Y+0.3/dy*math.sin(theta))] = 0.1*random.random()*value/(dx*dy)
                        
                    if X>=2 and X<self.matrix.shape[0]-2 and Y>=2 and Y<self.matrix.shape[1]-2:
                        for i in range(10):
                            theta = 2*i*math.pi/10
                            self.matrix[int(X+0.2/dx*math.cos(theta)),int(Y+0.2/dy*math.sin(theta))] = (0.2+0.1*random.random())*value/(dx*dy)
                
                    if X>=1 and X<self.matrix.shape[0]-1 and Y>=1 and Y<self.matrix.shape[1]-1:
                        for i in range(10):
                            theta = 2*i*math.pi/10
                            self.matrix[int(X+0.1/dx*math.cos(theta)),int(Y+0.1/dy*math.sin(theta))] = (0.6+0.1*random.random())*value/(dx*dy)
                
                    self.matrix[X,Y] = value/(dx*dy)
            
            # calculate the maxmium points
            points = model.process(self.matrix)
            # track the points:
            self.tracker.track(points)
            self.create_matplotlib()
            self.create_form()
            self.root.update()
            
    
    

    def create_matplotlib(self):
        #创建绘图对象f
        f=plt.figure(num=2,figsize=(8,6),dpi=80,frameon=True)
        sns.heatmap(self.matrix,cmap="cool")
        for j,point in enumerate(self.tracker.points):
            cpx, cpy = point.current_prediction[0], point.current_prediction[1] # 当前预测坐标
            xuxian_circle(cpx,cpy,3,color=point.color)
        for j,point in enumerate(self.tracker.points):
            cpx, cpy = point.current_measurement[0], point.current_measurement[1] # 当前预测坐标
            circle(cpx,cpy,3,color=point.color)
        plt.plot(*self.line)
        plt.close()
        self.number.config(text = f"总共{int(self.tracker.total_num/2)} 向左{int(self.tracker.left_num/2)} 向右{int(self.tracker.right_num/2)}")
        self.figure = f
        

    def create_form(self):
        #把绘制的图形显示到tkinter窗口上
        self.canvas=FigureCanvasTkAgg(self.figure,self.root)
        #以前的版本使用show()方法，matplotlib 2.2之后不再推荐show（）用draw代替，但是用show不会报错，会显示警告
        self.canvas.get_tk_widget().place(
            x=540,
            y=50,
            anchor="nw"
        )

if __name__=="__main__":
    window = tk.Tk()
    window.title('DEMO')
    window.geometry('1200x600')
    form=From(root = window)