from sqlmapmorty import *
from redisData import *
from urlparse import *
from hbases import *
from mysql import *
import time

def sqlmapRun():
    while True:
        if sqlmapHbase() is not None:
            if parQuery() is None:
                parNoneWrite()
                putData()
                delete()
                print('参数为空，删除url')
                continue
            elif 'true' is parContrast():
                putData()
                delete()
                print('数据已存在，删除url')
                continue
            elif None is parContrast():
                write()
                putData()
                taskid = createnewtast()
                url = setUrl(taskid, sqlmapUrl())
                setCookie(taskid, sqlmapCookie())
                starttask(taskid, url)
                print('新数据,开始SQLMAP扫描')
                delete()
                print('已发送至SQLMAP扫描，删除数据')
            while True:
                time.sleep(5)
                if len(taskresult(taskid)) != 0:
                    host = sqlmapHost().decode(encoding="utf-8")

                    if select_asset(host) is not None:
                        asset_id = select_asset(host)
                        j = taskresult(taskid)
                        url = j[0]['value']['url'] + '?' + j[0]['value']['query']
                        db_info = j[1]['value'][0]['dbms'], j[1]['value'][0]['dbms_version']

                        payload = []
                        for i in j[1]['value'][0]['data']:
                            pay = j[1]['value'][0]['data'][i]['payload']
                            payload.append(pay)
                        pay = payload,db_info

                        if select_vuln(url) is not True:
                            insert_vuln(taskid, pay, url, asset_id)
                            db.close()
                    else:
                        insert_asset(host)
                        db.close()
                    break
                else:
                    deletetask(taskid)
                    break
        else:
            time.sleep(3)
            print('----------------')
            continue
sqlmapRun()