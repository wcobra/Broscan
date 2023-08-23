from redisData import *
import hbase


zk = '10.0.19.48:2181'
conn = hbase.ConnectionPool(zk).connect()
awvsTable = conn['BAOFOO_SECURITY']['Test_Web_Info_add']

def awvsBase():
    awvsInfo = awvsTable.get(one_redis_key())
    return awvsInfo

def awvsHost():
    return awvsBase().get('info:host')

def awvsUri():
    return awvsBase().get('info:uri')

def awvsUrl():
    url = awvsHost() + awvsUri()
    return 'http://' + url.decode(encoding="utf-8")
