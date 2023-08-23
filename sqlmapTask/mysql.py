import pymysql
import datetime

db = pymysql.connect("10.0.221.16", "root", "root@Admin.com", "SeMF")

cursor = db.cursor()


def insert_asset(host):
    sql = 'insert into AssetManage_asset (asset_id,asset_out_id,asset_name,asset_key,asset_description,asset_score' \
             ',asset_status,asset_check	,asset_inuse,asset_starttime,asset_updatetime,user_email,asset_area_id' \
             ',asset_type_id) values ("%s",null,"sqlmap","%s",null,0,0,0,0,current_timestamp,' \
             'current_timestamp,null,null,14)' % (datetime.datetime.now().strftime('%Y%m%d%H%M%S'), host)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()

def select_asset(host):
    asset_key = 'select asset_key from AssetManage_asset where asset_key = "%s"' % (host)
    try:
        cursor.execute(asset_key)
        if cursor.fetchone() != None:
            asset_id = 'select `id` from AssetManage_asset where asset_key = "%s"' % (host)
            cursor.execute(asset_id)
            for id in cursor.fetchone():
                return id
    except:
        db.rollback()


def select_vuln(scopen):
    asset_key = 'select `scopen` from VulnManage_vulnerability_scan where scopen = "%s"' % (scopen)
    try:
        cursor.execute(asset_key)
        if cursor.fetchone() != None:
                return True
    except:
        db.rollback()


def insert_vuln(vuln_id,vuln_info,scopen,asset_id):
    sql = 'insert into VulnManage_vulnerability_scan (vuln_id,vuln_name,cve_name,vuln_type,`leave`,introduce' \
             ',vuln_info,scopen	,fix,fix_action,fix_status,create_data,update_data' \
             ',vuln_asset_id) values ("%s","SQL Injection",null,"sqlmap",3,"SQL Injection","%s","%s","修复方案",null,' \
             '2,current_timestamp,current_timestamp,%d)' % (vuln_id,vuln_info,scopen,asset_id)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
