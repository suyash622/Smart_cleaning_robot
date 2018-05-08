import numpy as np
import matplotlib.pyplot as plt
import math
import cv2
import time

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

fig2 = plt.figure(figsize=(10, 5))
bx = fig2.add_subplot(111)
bx.scatter(realpoints[:,0],realpoints[:,1])
bx.scatter(0,0,color = 'red')
bx.scatter(1,1,color = 'green')
plt.savefig("maptest2.png")


f = open("wab.txt","w+")
f.write("The Co-ordinates of features x, y, z , feature\n")
f.write("o:cup obstacle, b: ball, j:junk noise\n")

flag = 0
img = cv2.imread('maptest2.png')
for i in range(0,img.shape[0]):
	for j in range(0,img.shape[1]):
		if(img[i][j][2] == 255 and img[i][j][0] == 0 and img[i][j][1] == 0):
			origin = (j,i)
			flag = 1	
			break
	if(flag==1):
		break

flag = 0
for i in range(0,img.shape[0]):
	for j in range(0,img.shape[1]):
		if(img[i][j][2] == 0 and img[i][j][0] == 0 and img[i][j][1] > 0):
			oneone = (j,i)
			flag = 1	
			break
	if(flag==1):
		break		


dydx = (oneone[0] - origin[0],oneone[1] - origin[1])
# print(img.shape)

img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
i1 = cv2.medianBlur(img,5)
i2 = cv2.GaussianBlur(img,(3,3),0)


'''
# global thresholding
ret1,th1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
ret2,th2 = cv2.threshold(i1,127,255,cv2.THRESH_BINARY)
ret3,th3 = cv2.threshold(i2,127,255,cv2.THRESH_BINARY)
mega = np.c_[img,th1,th2,th3]
'''

'''
# adaptive mean thresholding
th1 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
th2 = cv2.adaptiveThreshold(i1,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
th3 = cv2.adaptiveThreshold(i2,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
mega = np.c_[img,th1,th2,th3]
'''


# adaptive gaussian thresholding
th1 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
th2 = cv2.adaptiveThreshold(i1,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
th3 = cv2.adaptiveThreshold(i2,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
mega = np.c_[img,th1,th2,th3]
'''
#Otsu
ret1,th1 = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
ret2,th2 = cv2.threshold(i1,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
ret3,th3 = cv2.threshold(i2,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
mega = np.c_[img,th1,th2,th3]
'''


#Contours
image, contours, hierarchy = cv2.findContours(th1,1,2)

centrad = np.zeros((len(contours),3))
actpoints = np.zeros((len(contours),3))

th2c = th1
j = 0
for i in range(0,len(contours)):
	(x,y),radius = cv2.minEnclosingCircle(contours[i])
	if(int(radius)>=8 and int(radius)<= 40):

		centrad[j,0] = int(x)
		centrad[j,1] = int(y)
		centrad[j,2] = int(radius)

		if(j>=1):
			flag = 0
			for k in range(0,j-1):
				if(abs(centrad[j,0] - centrad[k,0]) <= 2 and abs(centrad[j,1]- centrad[k,1]) <= 3):
					flag = 1
					break

			# print(flag)
			if(flag==0):
				
				actpoints[j,0] = float("{0:.2f}".format((x-origin[0])/dydx[0]))
				actpoints[j,1] = float("{0:.2f}".format((y-origin[1])/dydx[1]))
				th2c = cv2.circle(th2c,(int(x),int(y)),int(radius),(0,255,0),1)
				j = j+1

		if(j==0):
			actpoints[j,0] = float("{0:.2f}".format((x-origin[0])/dydx[0]))
			actpoints[j,1] = float("{0:.2f}".format((y-origin[1])/dydx[1]))
			th2c = cv2.circle(th2c,(int(x),int(y)),int(radius),(0,255,0),1)
			j = j+1

centrad = centrad[0:j]
actpoints = actpoints[0:j]


for i in range(0,len(actpoints)):
	l = []
	rad = centrad[i,2]
	for j in range(0,len(realpoints)):
		resx = float("{0:.2f}".format(abs((rad-origin[0])/dydx[0])))
		resy = float("{0:.2f}".format(abs((rad-origin[1])/dydx[0])))
		
		if (abs(actpoints[i,0] - realpoints[j,0]) <= 0.05 and abs(actpoints[i,1] - realpoints[j,1]) <= 0.05):
			l.append(realpoints[j,2])

	actpoints[i,2] = max(l)

	if(abs(actpoints[i,2])>=0.12):
		c = 'c'
	else:
		if(abs(actpoints[i,2])>=0.025 and abs(actpoints[i,2])<=0.06):
			c = 'b'
		else:
			c = 'j'

	f.write("%f %f %f %c\n" %(actpoints[i,0],actpoints[i,1],actpoints[i,2],c))



	'''if( resx<= 0.02  and  resy<= 0.02):
		actpoints[i,2] = realpoints[j,2]
		break
	'''

	'''	
	if( resx<= resx  and  resy<= resy):
		actpoints[i,2] = realpoints[j,2]
		print(actpoints[i,:],i)
		break	
	'''	

f.close()

print("Action Points sampled:")
print(actpoints)
print("Begining Path Planning")
time.sleep(1)
cv2.imwrite("thmp3.png",th2c)
# cv2.waitKey(0)
cv2.destroyAllWindows()