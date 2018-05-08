import http.client as httpc
import json

# http header
headers = { "charset" : "utf-8", "Content-Type": "application/json" }

pdata = {}
jdata = json.dumps(pdata, ensure_ascii = 'False')
conn = httpc.HTTPConnection("cerlab29.andrew.cmu.edu")
conn.request("POST", "/RSIoT-2018/rsiot06/rsiot06_url_r.php", jdata, headers) # read from DB
response = conn.getresponse()
result=response.read().decode()
pdata = json.loads(result)
#ht2 = time.time();
#print("%.3fsec" % (t2-t1))
#print(pdata)
outFile=open('download.txt','w')
print "Begining Uploading"
for line in pdata:
#    print(line)
    text=line['text']
    print("Uploaded "  + text)
    outFile.write(str(text))
    outFile.write('\n')
    
outFile.close()
