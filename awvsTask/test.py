import pymysql
import datetime

db = pymysql.connect("10.0.221.16", "root", "root@Admin.com", "SeMF")
cursor = db.cursor()
'''
select = "insert into AssetManage_asset (asset_id,asset_out_id	,asset_name,asset_key,asset_description,asset_score" \
         ",asset_status,asset_check	,asset_inuse,asset_starttime,asset_updatetime,user_email,asset_area_id" \
         ",asset_type_id) values ('%s',null,'test','%s',null,0,0,0,0,current_timestamp," \
         "current_timestamp,null,null,14)" % (datetime.datetime.now().strftime('%Y%m%d%H%M%S'),'ewrwevwqe3cdxs')
'''

select = "select asset_key from AssetManage_asset where asset_key = '10.6.52.47'"

try:
    cursor.execute(select)
    test = cursor.fetchone()
    if test != None:
        print(test)
    db.commit()
except:
    # 发生错误时回滚
    db.rollback()

# 关闭数据库连接
db.close()

