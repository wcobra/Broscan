from sqlmapmorty import *
from mysql import *
from hbases import *
import time

def sqlmapRun():
    taskid = createnewtast()
    url = setUrl(taskid, 'http://testphp.vulnweb.com/listproducts.php?artist=1&cat=1')
    #setCookie(taskid, sqlmapCookie())
    starttask(taskid, url)
    #print('开始SQLMAP扫描')
    while True:
        time.sleep(5)
        if len(taskresult(taskid)) != 0:
            host = 'testphp.vulnweb.com'    #sqlmapHost().decode(encoding="utf-8")
            if select_asset(host) is not None:
                asset_id = select_asset(host)
                j = taskresult(taskid)
                url = j[0]['value']['url'] + '?'+ j[0]['value']['query']
                db_info = j[1]['value'][0]['dbms'] , j[1]['value'][0]['dbms_version']
                payload = []
                for i in j[1]['value'][0]['data']:
                    pay = j[1]['value'][0]['data'][i]['payload']
                    payload.append(pay)
                pay = payload,db_info
                if select_vuln(url) is not True:
                    insert_vuln(taskid,pay,url,asset_id)
                    db.close()
            else:
                insert_asset(host)
                db.close()
            break
        else:
            deletetask(taskid)
            break
sqlmapRun()