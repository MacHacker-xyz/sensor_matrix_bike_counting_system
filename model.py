from os import sep
import numpy as np
from numpy.core.fromnumeric import argmax
result_shape = None
direction = None
data_shape = None

def step(result):
    temp_result = np.zeros(data_shape)
    result = direction*result
    for i in range(3):
        for j in range(3):
            temp_result[i:i+result_shape[0],j:j+result_shape[1]] += result[np.arange(9).reshape(3,3)[i,j],:,:]
            
    result = temp_result[1:1+result_shape[0],1:1+result_shape[1]]
    return result
    

def process(data):
    global result_shape
    global direction
    global data_shape
    result_shape = data.shape
    data = np.pad(data,((1,1),(1,1)),'constant',constant_values = (0,0))
    data_shape = data.shape
    result = np.ones(result_shape)
    last_result = np.ones(result_shape)
    
    
    
    direction = np.zeros((*result_shape,9))
    a = np.array([1,2,3,4,0,5,6,7,8]).reshape(3,3)
    for i in range(3):
        for j in range(3):
            direction[:,:,a[i,j]] = data[i:i+result_shape[0],j:j+result_shape[1]]
    indexes = np.argmax(direction,axis=2)
    
    direction = np.zeros((*result_shape,9))
    for i in range(result_shape[0]):
        for j in range(result_shape[1]):
            direction[i,j,indexes[i,j]]=1
    direction = direction.transpose(2,0,1)
    temp = np.zeros(direction.shape)
    a = a.reshape(9,)
    for i in range(9):
        temp[i] = direction[a[i]]
    direction = temp
    
    
    while True:
        
        last_result = result
        result = step(last_result)
        if np.sum(last_result!= result)==0:
            break
    temp = []
    for i in range(result_shape[0]):
        for j in range(result_shape[1]):
            if result[i,j]>1:
                temp.append((i,j))
                
    return temp

if __name__=="__main__":
    image = np.loadtxt("/Users/houzhaobang/Desktop/sensor_matrix_simulation/data/images/445.txt",delimiter=',')
    data = process(image)
    print(data)