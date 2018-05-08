import http.client as httpc
import json
import time
# http header
headers = { "charset" : "utf-8", "Content-Type": "application/json" }

inFile=open('upload2.txt','rt')
inString=inFile.read()
#print inString
stringList=inString.splitlines()
print "Uploading this to server"
print(stringList)
time.sleep(1)
for line in stringList:
    
    #write
    text=line
#    print(text)
    pdata={"text":text}
    jdata = json.dumps(pdata, ensure_ascii = 'False')
    conn = httpc.HTTPConnection("cerlab29.andrew.cmu.edu")
    conn.request("POST", "/RSIoT-2018/rsiot06/rsiot06_url_w.php", jdata, headers) # write to DB
    response = conn.getresponse()
    #print(response.read().decode())
print ("Uploading completed!!")