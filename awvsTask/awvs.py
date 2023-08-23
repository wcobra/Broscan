import json
import ssl
import urllib.request
import os


ssl._create_default_https_context = ssl._create_unverified_context

IP = '10.6.52.47'
API_KEY = '1986ad8c0a5b3df4d7028d5f3c06e936c7cb8368cf5484604b4a0c8a93cacc6cf'


def add_target(address,description):
    url = 'https://' + IP + ':3443/api/v1/targets'
    headers = {"X-Auth": API_KEY, "content-type": "application/json", 'User-Agent': 'curl/7.53.1'}
    values = {
        'address': address,
        'description': description,
        'criticality': 10,
    }
    data = bytes(json.dumps(values), 'utf-8')
    request = urllib.request.Request(url, data, headers)
    print(url,data,headers)
    html = urllib.request.urlopen(request).read().decode('utf-8')
    j = json.loads(html)
    return j['target_id']


def one_target(target_id):
    url = 'https://' + IP + ':3443/api/v1/targets/' + target_id
    headers = {"X-Auth": API_KEY, "content-type": "application/json", 'User-Agent': 'curl/7.53.1'}
    request = urllib.request.Request(url=url, headers=headers)
    html = urllib.request.urlopen(request).read().decode('utf-8')
    j = json.loads(html)
    return j['last_scan_session_status'],j['last_scan_id'],j['last_scan_session_id']


def start_target(target_id):
    url = 'https://' + IP + ':3443/api/v1/scans'
    headers = {"X-Auth": API_KEY, "content-type": "application/json", 'User-Agent': 'curl/7.53.1'}
    values = {
        'target_id': target_id,
        'profile_id': '11111111-1111-1111-1111-111111111111',
        'schedule': {
            'disable': False,
            'start_date': None,
            'time_sensitive': False
        }
    }
    data = bytes(json.dumps(values), 'utf-8')
    request = urllib.request.Request(url, data, headers)
    html = urllib.request.urlopen(request).read().decode('utf-8')
    return html


def login_sequence(target_id,fileName):
    url = 'https://' + IP + ':3443/api/v1/targets/' + target_id + '/configuration/login_sequence'
    headers = {"X-Auth": API_KEY, "content-type": "application/json", 'User-Agent': 'curl/7.53.1'}
    values = {'name':fileName,'size':os.stat(fileName).st_size}
    data = bytes(json.dumps(values), 'utf-8')
    request = urllib.request.Request(url, data, headers)
    html = urllib.request.urlopen(request).read().decode('utf-8')
    j = json.loads(html)
    return j['upload_url']

def uploads(upload_url,fileName):
    url = 'https://' + IP + ':3443' + upload_url
    headers = {"X-Auth": API_KEY, "content-type": "application/octet-stream", 'User-Agent': 'curl/7.53.1',
               'Content-Disposition': 'attachment; filename="%s"' % (fileName),
               'Content-Range': 'bytes 0-%d/%d'% (os.stat(fileName).st_size-1,os.stat(fileName).st_size)}
    data = bytes(open(fileName,'r',encoding='utf-8').read(),'utf-8')
    request = urllib.request.Request(url, data, headers)
    code = urllib.request.urlopen(request).getcode()
    return code


def configuration(target_id):
    url = 'https://' + IP + ':3443/api/v1/targets/' + target_id + '/configuration'
    headers = {"X-Auth": API_KEY, "content-type": "application/json", 'User-Agent': 'curl/7.53.1'}
    values = {'login':{'kind':'sequence'}}
    data = bytes(json.dumps(values), 'utf-8')
    request = urllib.request.Request(url, data, headers,method = 'PATCH')
    code = urllib.request.urlopen(request).getcode()
    return code

def target_status(last_scan_id):
    url = 'https://' + IP + ':3443/api/v1/scans/' + last_scan_id
    headers = {"X-Auth": API_KEY, "content-type": "application/json", 'User-Agent': 'curl/7.53.1'}
    request = urllib.request.Request(url=url, headers=headers)
    html = urllib.request.urlopen(request).read().decode('utf-8')
    j = json.loads(html)
    low =  j['current_session']['severity_counts']['low']
    info = j['current_session']['severity_counts']['info']
    medium = j['current_session']['severity_counts']['medium']
    high = j['current_session']['severity_counts']['high']
    return low+info+medium+high

def get_target_result(last_scan_id, last_scan_session_id):
    url = 'https://' + IP + ':3443/api/v1/scans/' + last_scan_id + '/results/' + last_scan_session_id + '/vulnerabilities '
    headers = {"X-Auth": API_KEY, "content-type": "application/json", 'User-Agent': 'curl/7.53.1'}
    request = urllib.request.Request(url=url, headers=headers)
    html = urllib.request.urlopen(request).read().decode('utf-8')
    print(html)


def vulnerabilities(last_scan_id, last_scan_session_id, previous_cursor ):
    url = 'https://%s:3443/api/v1/scans/%s/results/%s/vulnerabilities?c=%d&q=status:open' % (
        IP, last_scan_id,last_scan_session_id,previous_cursor
    )
    headers = {"X-Auth": API_KEY, "content-type": "application/json", 'User-Agent': 'curl/7.53.1'}
    request = urllib.request.Request(url=url, headers=headers)
    html = urllib.request.urlopen(request).read().decode('utf-8')
    j = json.loads(html)
    return j['vulnerabilities']

def one_vuln(last_scan_id, last_scan_session_id, vuln_id ):
    url = 'https://%s:3443/api/v1/scans/%s/results/%s/vulnerabilities/%s' % (
        IP, last_scan_id,last_scan_session_id,vuln_id
    )
    headers = {"X-Auth": API_KEY, "content-type": "application/json", 'User-Agent': 'curl/7.53.1'}
    request = urllib.request.Request(url=url, headers=headers)
    html = urllib.request.urlopen(request).read().decode('utf-8')
    j = json.loads(html)
    return j


'''
def getReport(last_scan_id):
    url = 'https://' + IP + ':3443/api/v1/reports'
    headers = {"X-Auth": API_KEY, "content-type": "application/json", 'User-Agent': 'curl/7.53.1'}
    values = {
        'template_id': '11111111-1111-1111-1111-111111111111',
        'source': {
            'list_type': 'scans',
            'id_list': [last_scan_id],
        }
    }
    data = bytes(json.dumps(values), 'utf-8')
    request = urllib.request.Request(url, data, headers)
    html = urllib.request.urlopen(request).getheader('Location').replace('/api/v1/reports/','/reports/download/')
    #html = urllib.request.urlopen(request).read().decode('utf-8')
    return html
    
    
def profiles_list():
    url = 'https://' + IP + ':3443/api/v1/scanning_profiles'
    headers = {"X-Auth": API_KEY, "content-type": "application/json", 'User-Agent': 'curl/7.53.1'}
    request = urllib.request.Request(url=url, headers=headers)
    html = urllib.request.urlopen(request).read().decode('utf-8')
    return html
    
    
def get_target_list():
    url = 'https://' + IP + ':3443/api/v1/targets'
    headers = {"X-Auth": API_KEY, "content-type": "application/json", 'User-Agent': 'curl/7.53.1'}
    request = urllib.request.Request(url=url, headers=headers)
    html = urllib.request.urlopen(request).read().decode('utf-8')
    return html
    
def stop_target(target_id):
    url = 'https://' + IP + ':3443/api/v1/scans/' + target_id + '/abort'
    headers = {"X-Auth": API_KEY, "content-type": "application/json", 'User-Agent': 'curl/7.53.1'}
    request = urllib.request.Request(url=url, headers=headers)
    html = urllib.request.urlopen(request).read().decode('utf-8')
    print(html)

'''