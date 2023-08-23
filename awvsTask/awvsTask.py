from awvs import *
from urlparse import *
from redisData import *
import time

def awvsRun():
    while True:
        if one_redis_key() is not None:
            time.sleep(2)
            target_id = add_target(awvsUrl(),'AWVS')
            last_scan_id = one_target(target_id)[1]
            last_scan_session_id = one_target(target_id)[2]
            start_target(target_id)
            print('开始扫描')
            if one_target(target_id)[0] is not None:
                if 'failed' in one_target(target_id)[0]:
                    print('扫描失败')
                    break
            if awvsParQuery() is None:
                awvsNoneWrite()
                print('写入空参数')
            else:
                for k in awvsKeys():
                    redis.hset(one_redis_key(), k, 'AWVS')
                print('写入awvs标识')
        while True:
            time.sleep(3)
            if 'completed' in one_target(target_id)[0]:
                previous_cursor = target_status(last_scan_id)
                for i in range(0, previous_cursor):
                    a = vulnerabilities(last_scan_id,last_scan_session_id,i)
                    for n in a:
                        print(previous_cursor,one_vuln(last_scan_id, last_scan_session_id,n['vuln_id']))
                break
            elif 'aborting' in one_target(target_id)[0]:
                print('停止扫描')
                break
            elif 'processing' in one_target(target_id)[0]:
                print('正在扫描')
awvsRun()
