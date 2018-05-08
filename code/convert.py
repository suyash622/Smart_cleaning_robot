
from matplotlib import pyplot as plt
import numpy as np
infile = open('points_inliers_r.pcd','rt')
data = infile.readlines()
data = data[11:]
data = [k.split(" ") for k in data]
for i in range(0,len(data)):
    data[i] = [float(k) for k in data[i]]
    
realpoints = np.zeros((len(data),3))
    

for i in range(0,len(data)):
    realpoints[i,0] = data[i][0]
    realpoints[i,1] = data[i][1]
    realpoints[i,2] = data[i][2]

plt.plot(realpoints[:,0],realpoints[:,1])
plt.savefig('map.png')