import math
import numpy as np
import random
import KM
from PIL import Image
import matplotlib.pyplot as plt
import seaborn as sns
import model



class bike:
    def __init__(self, x_0, y_0, v, theta, l, G,  sensor_matrix):
        self.x = x_0
        self.y = y_0
        self.theta = theta
        self.l = l
        self.v_x = -v*math.sin(theta)
        self.v_y = v*math.cos(theta)
        self.front_x = x_0-0.5*l*math.sin(theta)
        self.front_y = y_0+0.5*l*math.cos(theta)
        self.back_x = x_0+0.5*l*math.sin(theta)
        self.back_y = y_0-0.5*l*math.cos(theta)
        self.G = G
        self.sensor_matrix = sensor_matrix
        sensor_matrix.objects.append(self)
        
    def run(self,dt):
        self.x = self.x+self.v_x*dt
        self.y = self.y+self.v_y*dt
        self._update(dt)
    
    def _update(self,dt):
        self.front_x = self.front_x+self.v_x*dt
        self.front_y = self.front_y+self.v_y*dt
        self.back_x = self.back_x+self.v_x*dt
        self.back_y = self.back_y+self.v_y*dt
    
    def measure(self,i):
        result = {}
        result[(self.front_x, self.front_y)] = self.G/2
        result[(self.back_x, self.back_y)] = self.G/2
        for (x,y), value in result.items():
            flag = 0
            X,Y = int(x/self.sensor_matrix.dx),int(y/self.sensor_matrix.dy)
            if X>=0 and X<self.sensor_matrix.params.shape[0] and Y>=0 and Y<self.sensor_matrix.params.shape[1]:
                
                if X>=3 and X<self.sensor_matrix.params.shape[0]-3 and Y>=3 and Y<self.sensor_matrix.params.shape[1]-3:
                    for i in range(10):
                        theta = 2*i*math.pi/10
                        self.sensor_matrix.params[int(X+0.3/self.sensor_matrix.dx*math.cos(theta)),int(Y+0.3/self.sensor_matrix.dy*math.sin(theta))] = 0.1*random.random()*value/(self.sensor_matrix.dx*self.sensor_matrix.dy)
                        
                if X>=2 and X<self.sensor_matrix.params.shape[0]-2 and Y>=2 and Y<self.sensor_matrix.params.shape[1]-2:
                    for i in range(10):
                        theta = 2*i*math.pi/10
                        self.sensor_matrix.params[int(X+0.2/self.sensor_matrix.dx*math.cos(theta)),int(Y+0.2/self.sensor_matrix.dy*math.sin(theta))] = (0.2+0.1*random.random())*value/(self.sensor_matrix.dx*self.sensor_matrix.dy)
                
                if X>=1 and X<self.sensor_matrix.params.shape[0]-1 and Y>=1 and Y<self.sensor_matrix.params.shape[1]-1:
                    for i in range(10):
                        theta = 2*i*math.pi/10
                        self.sensor_matrix.params[int(X+0.1/self.sensor_matrix.dx*math.cos(theta)),int(Y+0.1/self.sensor_matrix.dy*math.sin(theta))] = (0.6+0.1*random.random())*value/(self.sensor_matrix.dx*self.sensor_matrix.dy)
                
                self.sensor_matrix.params[X,Y] = value/(self.sensor_matrix.dx*self.sensor_matrix.dy)
                
                
                    
class sensor_matrix:
    def __init__(self, height, width, dx, dy):
        self.height = height
        self.width = width
        self.dx = dx
        self.dy = dy
        self.objects = []
        self.params = np.zeros(shape=(int(self.width/self.dx), int(self.height/self.dy)), dtype=np.float64)
        self.params1 = np.zeros(shape=(int(self.width/self.dx), int(self.height/self.dy)), dtype=np.float64)
        
    def run(self,dt):
        for bike in self.objects:
            bike.run(dt)
    
    def show(self,i,Track):
        # track the points
        Track.track(model.process(self.params))
    
    def measure(self,i):
        self.params = np.zeros(shape=(int(self.width/self.dx), int(self.height/self.dy)), dtype=np.float64)
        for bike in self.objects:
            bike.measure(i)
    

def make_bike_1(height, width, sensor_matrix):
    # define some initial conditions:
    # please set some posible range
    v_max = 6
    v_min = 2
    x_max = width
    x_min = 0
    y_max = -height
    y_min = -2*height
    l_max = 1.1
    l_min = 0.9
    G_max = 75
    G_min = 110
    
    # then generate the initial position and velocity
    x_0 = random.uniform(x_min,x_max)
    y_0 = random.uniform(y_min,y_max)
    v = random.uniform(v_min,v_max)
    l = random.uniform(l_min,l_max)
    G = random.uniform(G_min,G_max)
    
    # then we can calculate the possible directions:
    theta_max = math.atan(x_0/(2*height-y_0))
    theta_min = math.atan((x_0-width)/(2*height-y_0))
    theta = random.uniform(theta_min,theta_max)
    
    # new the bike
    _=bike(x_0,y_0,v, theta, l, G, sensor_matrix)


def make_bike_2(height, width, sensor_matrix):
    # define some initial conditions:
    # please set some posible range
    v_max = 6
    v_min = 1
    x_max = width
    x_min = 0
    y_max = 3*height
    y_min = 2*height
    l_max = 1.1
    l_min = 0.9
    G_max = 75
    G_min = 110
    
    # then generate the initial position and velocity
    x_0 = random.uniform(x_min,x_max)
    y_0 = random.uniform(y_min,y_max)
    v = random.uniform(v_min,v_max)
    l = random.uniform(l_min,l_max)
    G = random.uniform(G_min,G_max)
    
    # then we can calculate the possible directions:
    theta_max = math.atan(x_0/(-y_0))
    theta_min = math.atan((x_0-width)/(-y_0))
    theta = random.uniform(math.pi-theta_min,math.pi - theta_max)
    
    # new the bike
    _=bike(x_0,y_0,v, theta, l, G, sensor_matrix)



if __name__ == "__main__":
    Track = KM.Tracker()
    # define the time you want to simulate
    total_time = 100
    
    # define the time scale between each frame
    time_scale = 0.1
    
    # some parameters 
    height = 10
    width = 10
    
    # initial some classes
    Mat = sensor_matrix(height=height, width=width, dx=0.1, dy=0.1)
    
    for i in range(0,int(total_time/time_scale)):
        t = i*time_scale
        
        # control the make bike frequancy
        if i%(int(4/time_scale))==0 or  i%(int(4/time_scale))==1:
            make_bike_1(height,width,Mat)
        if i%(int(4/time_scale))==2 or i%(int(4/time_scale))==3 :
            make_bike_2(height,width,Mat)
        
        # run the model and params
        Mat.run(dt=time_scale)
        Mat.measure(i)
        Mat.show(i)
        