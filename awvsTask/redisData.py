from urlparse import *
import redis


redis = redis.Redis(host='10.0.221.16', port=6379,charset='utf-8',decode_responses=True)


# 写入AWVS标识
def awvsNoneWrite():
    redis.hset(one_redis_key(), 'SQLMAP', 'AWVS')


def one_redis_key():
    for key in redis.keys():
        for val in redis.hvals(key):
            if 'SQLMAP' in val:
                return key