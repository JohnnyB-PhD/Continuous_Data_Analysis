import math
import numpy as np
import sys

data = np.loadtxt(sys.argv[1], delimiter="\t", skiprows=1)
output = sys.argv[2]
speed = np.zeros(data.shape[0])
for i in range(data.shape[0]):
    if i == 0:
        continue
    distance = math.sqrt((data[i,1]-data[i-1,1])**2 + (data[i,2]-data[i-1,2])**2)
    time = data[i,0] - data[i-1,0]
    speed[i] = distance/time
speed[speed > 500] = 0
time_start = []
time_stop = []
time_speed = []
std_error = []
startpoint = -1
endpoint = -1
total_time = 0
total_distance = 0
for i in range(len(speed)):
    if i == 0:
        continue
    if speed[i] == 0 and startpoint == -1:
        startpoint = i
        continue
    if speed[i-1] == 0 and speed[i] == 0:
        startpoint = -1
    if startpoint > -1 and speed[i] == 0:
        endpoint = i
    if startpoint > -1 and endpoint > -1:
        move_speed =  []
        for j in range(startpoint, endpoint):
            block_time = abs(data[j,0] - data[j-1,0])
            block_distance = math.sqrt((data[j,1]-data[j-1,1])**2 + (data[j,2]-data[j-1,2])**2)
            move_speed.append(block_distance/block_time)
            total_time += block_time
            total_distance += block_distance
        if total_time > 0.5 and total_distance > 0.5:
            time_start.append(data[startpoint,0])
            time_stop.append(data[endpoint,0])
            time_speed.append(np.mean(np.array(move_speed)))
            std_error.append(np.std(np.array(move_speed))/len(move_speed))
        total_time = 0
        total_distance = 0
        startpoint = -1
        endpoint = -1
out_array = np.transpose(np.array([time_start, time_stop, time_speed, std_error]))
out = open(output, 'w')
out.write("Time Start\tTime Stop\tAverage Speed\tStd Error\n")
out.close()
out = open(output, 'ab')
np.savetxt(out, out_array, delimiter="\t")
out.close()
