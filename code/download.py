import http.client as httpc
import json
import time

# http header
headers = { "charset" : "utf-8", "Content-Type": "application/json" }

pdata = {}
jdata = json.dumps(pdata, ensure_ascii = 'False')
conn = httpc.HTTPConnection("cerlab29.andrew.cmu.edu")
conn.request("POST", "/RSIoT-2018/rsiot06/rsiot06_points_inliers_r.php", jdata, headers) # read from DB
response = conn.getresponse()
result=response.read().decode()
pdata = json.loads(result)
#ht2 = time.time();
#print("%.3fsec" % (t2-t1))
#print(pdata)
data=pdata["pos_array"]

outFile=open('points_inliers_r.pcd','w')
no = 0
for point in data:
	no+=1
	coord=point["pos"]
	posx=coord[0]
	posy=coord[1]
	posz=coord[2]

	outFile.write("%0.2f %0.2f %0.2f\n" % (posx, posy, posz))
	
outFile.close()


print "Download has been succesfull, %d points sampled" %no
time.sleep(2)