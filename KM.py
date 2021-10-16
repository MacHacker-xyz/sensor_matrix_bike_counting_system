import cv2
import numpy as np
import math
from munkres import Munkres



COLORS = ['r','g','b','m','y','c']

class Point():
    def __init__(self,x,y,tracker,line,color):
        # 这里单独生成卡拉曼滤波器
        self.last_measurement = np.array((x,y), np.float32)
        self.current_measurement = np.array((x,y), np.float32)
        self.last_prediction = np.array((x,y), np.float32)
        self.current_prediction = np.array((x,y), np.float32)
        self.kalman = cv2.KalmanFilter(4, 2) # 4：状态数，包括（x，y，dx，dy）坐标及速度（每次移动的距离）；2：观测量，能看到的是坐标值
        self.kalman.measurementMatrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0]], np.float32) # 系统测量矩阵
        self.kalman.transitionMatrix = np.array([[1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0], [0, 0, 0, 1]], np.float32) # 状态转移矩阵
        self.kalman.processNoiseCov = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]], np.float32)*0.03 # 系统过程噪声协方差
        self.line = line
        self.tracker = tracker 
        self.color = color
        
    def update(self,x,y):
        # 更新当前位置，并且计算得出下一时刻位置的预测值
        self.last_prediction = self.current_prediction # 把当前预测存储为上一次预测
        self.last_measurement = self.current_measurement # 把当前测量存储为上一次测量
        self.current_measurement = np.array([[np.float32(x)], [np.float32(y)]]) # 当前测量
        self.kalman.correct(self.current_measurement) # 用当前测量来校正卡尔曼滤波器
        self.current_prediction = self.kalman.predict() # 计算卡尔曼预测值，作为当前预测
        
        # 比对看看点是否穿过了直线：
        x1, y1 = self.last_measurement[0],self.last_measurement[1]
        x2, y2 = self.current_measurement[0],self.current_measurement[1]
        temp1 = (self.line[1][0]-self.line[1][1])*(y1-self.line[0][0])-(x1-self.line[1][0])*(self.line[0][0]-self.line[0][1])
        temp2 = (self.line[1][0]-self.line[1][1])*(y2-self.line[0][0])-(x2-self.line[1][0])*(self.line[0][0]-self.line[0][1])
        
        if x1>=0 and x1<100 and x2>=0 and x2<100 and y1>=0 and y1<100 and y2>=0 and y2<100:
            if temp1*temp2<=0:
                if temp1>0:
                    self.tracker.right_num+=1
                    self.tracker.total_num+=1
                elif temp2>=0:
                    self.tracker.left_num+=1
                    self.tracker.total_num+=1
            

class Tracker():
    def __init__(self,line):
        self.points = []
        self.line = line #[[x1,x2],[y1,y2]]
        self.total_num = 0
        self.left_num = 0
        self.right_num = 0
        self.count = 0
        
    def track(self,new_points):
        # new_points形如[(1,2),(10,10)]记录个点的位置
        distance_matrix = []
        for point in self.points:
            cpx, cpy = point.current_prediction[0], point.current_prediction[1] # 当前预测坐标
            distance = []
            for new_point in new_points:
                distance.append(math.sqrt((new_point[0]-cpx)**2+(new_point[1]-cpy)**2))
            distance_matrix.append(distance)
        
        m = Munkres()
        if len(distance_matrix)!=0:
            indexes = m.compute(distance_matrix)
            
        else:
            indexes = []
        
        if len(new_points)==len(self.points):
            for i,j in indexes:
                self.points[i].update(*new_points[j])
                
                
        elif len(new_points)>len(self.points):
            temp = [i for i in range(len(new_points))]
            for i,j in indexes:
                temp.remove(j)
                self.points[i].update(*new_points[j])
                
            for i in temp:
                p=Point(*new_points[i],self,self.line, COLORS[self.count%len(COLORS)])
                self.count+=1
                p.update(*new_points[i])
                self.points.append(p)
                
        elif len(new_points)<len(self.points):
            temp = [i for i in range(len(self.points))]
            for i,j in indexes:
                temp.remove(i)
                self.points[i].update(*new_points[j])
            for i in reversed(temp):
                self.points.pop(i)
        
