import json
import urllib.request


URL = 'http://127.0.0.1:8775'


def createnewtast():
    uri = '/task/new'
    request = urllib.request.Request(URL + uri)
    html = urllib.request.urlopen(request).read().decode('utf-8')
    j = json.loads(html)
    if j['success']==True:
        return j['taskid']
    else:
        return 'error'


def deletetask(taskid):
    uri = '/task/' + taskid + '/delete'
    request = urllib.request.Request(URL + uri)
    html = urllib.request.urlopen(request).read().decode('utf-8')
    return html

def setCookie(taskid,cookie):
    uri = '/option/' + taskid + '/set'
    values = {"cookie": cookie}
    data = bytes(json.dumps(values), 'utf-8')
    requestheader = {"Content-Type": "application/json"}
    request = urllib.request.Request(URL + uri, headers=requestheader, data=data)
    html = urllib.request.urlopen(request).read().decode("utf-8")
    return cookie

def setHeader(taskid,headers):
    uri = '/option/' + taskid + '/set'
    values = {"headers": headers}
    data = bytes(json.dumps(values), 'utf-8')
    requestheader = {"Content-Type": "application/json"}
    request = urllib.request.Request(URL + uri, headers=requestheader, data=data)
    html = urllib.request.urlopen(request).read().decode("utf-8")
    return headers

def setUrl(taskid,url):
    uri = '/option/' + taskid + '/set'
    values = {"url": url}
    data = bytes(json.dumps(values), 'utf-8')
    requestheader = {"Content-Type": "application/json"}
    request = urllib.request.Request(URL + uri, headers=requestheader, data=data)
    html = urllib.request.urlopen(request).read().decode("utf-8")
    return url

def starttask(taskid,dsturl):
    uri = '/scan/' + taskid + '/start'
    data = json.dumps({"url": "{}".format(dsturl)}).encode("utf-8")
    requestheader = {"Content-Type": "application/json"}
    request = urllib.request.Request(URL + uri, headers=requestheader, data=data)
    html = urllib.request.urlopen(request).read().decode("utf-8")
    return html

def taskstatus(taskid):
    uri = '/scan/' + taskid + '/status'
    request = urllib.request.Request(URL + uri)
    html = urllib.request.urlopen(request).read().decode('utf-8')
    j = json.loads(html)
    return j['status']

def taskresult(taskid):
    uri = '/scan/' + taskid + '/data'
    request = urllib.request.Request(URL + uri)
    html = urllib.request.urlopen(request).read().decode('utf-8')
    j=json.loads(html)
    return j['data']