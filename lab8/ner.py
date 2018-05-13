user="mojadresemail"
lpmn="any2txt|wcrft2|liner2({\"model\":\"n82\"})"
import json
import glob
from urllib.request import urlopen, Request
import os
import time
url="http://ws.clarin-pl.eu/nlprest2/base"

def upload(file):
        with open (file, "rb") as myfile:
            doc=myfile.read()
            myfile.close()
        print("uploading")
        return urlopen(Request(url+'/upload/',doc,{'Content-Type': 'binary/octet-stream'})).read();

def process(data):
        doc=json.dumps(data).encode()
        taskid = urlopen(Request(url+'/startTask/',doc,{'Content-Type': 'application/json'})).read();
        time.sleep(0.2);

        request_url = url+'/getStatus/' + taskid.decode('utf-8')

        resp = urlopen(Request(request_url));
        data=json.load(resp)
        while data["status"] == "QUEUE" or data["status"] == "PROCESSING" :
            print(data["status"])
            time.sleep(2);
            resp = urlopen(Request(request_url));
            data=json.load(resp)
        if data["status"]=="ERROR":
            print("Error "+data["value"]);
            return None;
        return data["value"]

def upload_process(file_name):
    fileid=upload(file_name)
    fileid = fileid.decode('utf-8')
    data={'lpmn':lpmn,'user':user,'file':fileid}
    data=process(data)
    print("processed")
    data=data[0]["fileID"];
    content = urlopen(Request(url+'/download'+data)).read();
    print("open content")
    return content
