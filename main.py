import simulation
import KM
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 这里定义直线
line = [[25,25],[0,50]] #[[x1,x2],[y1,y2]]

# define the tracker object
Track = KM.Tracker(line=line)
# define the time you want to simulate
total_time = 100
    
# define the time scale between each frame
time_scale = 0.1
    
# some parameters 
height = 10
width = 10
    
# initial some classes
Mat = simulation.sensor_matrix(height=height, width=width, dx=0.2, dy=0.2)


def circle(x,y,r,color='k',count=1000):
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
 
for i in range(0,int(total_time/time_scale)):
    t = i*time_scale
    # control the make bike frequancy
    if i%(int(4/time_scale))==0 or i%(int(4/time_scale))==2:
        simulation.make_bike_1(height,width,Mat)
    #if i%(int(4/time_scale))==1 or i%(int(4/time_scale))==3 :
        #simulation.make_bike_2(height,width,Mat)
    # run the model and params
    Mat.run(dt=time_scale)
    Mat.measure(i)
    # visualization
    Mat.show(i,Track=Track)
    
    sns.heatmap(data = Mat.params, cmap="YlOrRd")
    # show some pictures
    
    for j,point in enumerate(Track.points):
        cpx, cpy = point.current_prediction[0], point.current_prediction[1] # 当前预测坐标
        xuxian_circle(cpx,cpy,3,color=point.color)

    for j,point in enumerate(Track.points):
        cpx, cpy = point.current_measurement[0], point.current_measurement[1] # 当前预测坐标
        circle(cpx,cpy,3,color=point.color)

    plt.plot(*line)
    
    plt.text(0,0, f"TOTAL{Track.total_num}  LEFT{Track.left_num} RIGHT{Track.right_num}", color = "r",size = 15)
    plt.savefig("picture/{}.jpg".format(i))
    
    plt.close()
    