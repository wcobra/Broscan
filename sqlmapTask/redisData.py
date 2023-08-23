from urlparse import *
import redis


redis = redis.Redis(host='10.0.221.16', port=6379,charset='utf-8',decode_responses=True)

# 写入SQLMAP标识
def write():
    for k in parame().query.keys():
        redis.hset(sqlmapHbase().key, k, 'SQLMAP')


def parNoneWrite():
    redis.hset(sqlmapHbase().key, 'SQLMAP', 'SQLMAP')

parkey = []
def keys():
    for k in redis.hkeys(sqlmapHbase().key):
        parkey.append(k)
        parkey.sort()
    return parkey

#参数对比
def parContrast():
    if parQuery() is not None:
        for item in parQuery():
            if item in keys():
                return 'true'
