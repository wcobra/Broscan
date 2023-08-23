import hbase
from redisData import *


zk = '10.0.19.48:2181'
conn = hbase.ConnectionPool(zk).connect()
table = conn['BAOFOO_SECURITY']['Test_Web_Info_add']
awvsTable = conn['BAOFOO_SECURITY']['Test_Web_Info']

def sqlmapHbase():
    info = table.get_one()
    return info

def sqlmapHost():
    return sqlmapHbase().get('info:host')

def sqlmapUri():
    return sqlmapHbase().get('info:uri')

def sqlmapCookie():
    if sqlmapHbase().get('info:cookie') is not None:
        return sqlmapHbase().get('info:cookie').decode(encoding="utf-8")

def access_token():
    if sqlmapHbase().get('info:access_token') is not None:
        return sqlmapHbase().get('info:access_token').decode(encoding="utf-8")

def authorization():
    if sqlmapHbase().get('info:authorization') is not None:
        return sqlmapHbase().get('info:authorization').decode(encoding="utf-8")

def delete():
    table.delete(sqlmapHbase().key)

def putData():
    for keys in sqlmapHbase().keys():
        column = keys
        awvsTable.put(hbase.Row(
            sqlmapHbase().key, {
                column: sqlmapHbase().get(column)
            }
        ))

def sqlmapUrl():
    url = sqlmapHost() + sqlmapUri()
    return 'http://' + url.decode(encoding="utf-8")

