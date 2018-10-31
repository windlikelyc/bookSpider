# -*- coding: UTF-8 -*-
# 标签数量总共有7078 个，但是出现次数大于 x 次的有 y 个（30，175），（20，261），（10，486）
import codecs

import pymysql
import time
import random
from datetime import datetime, timedelta
conn = pymysql.connect(host='39.106.39.216',
                       user='root',
                       passwd="admin123",
                       db='doubandb_test',
                       port=3306,
                       charset='utf8')
cursor = conn.cursor()


sql = "SELECT user_id,count(*) AS c FROM book_comments GROUP BY user_id HAVING  c  > 5 ORDER BY c DESC"
tag_dict = {}


bb = set()
try:
    cursor.execute(sql)
    results = cursor.fetchall()
    bidset =  set()
    for row in results:
        bidset.add(row[0])
    ll = list(bidset)

    for i in range(len(ll)): # 遍历活跃用户
        sql2 = "SELECT * FROM book_comments WHERE user_id = %s"%ll[i]
        cursor.execute(sql2)
        rrr = cursor.fetchall()
        for o in rrr:
            bb.add(o[3])
    bb = list(bb)
    for z in range(len(bb)):
        pass
except Exception as e:
    print str(e)

