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

fo = codecs.open('book_id_map.txt','r',encoding='utf-8')

book_id_to_num = {} # 就是一个
book_id_to_tag_str = {}

book_author_to_num = {}

user_id_to_num = {}
user_id_to_num_index = 0

for line in fo.readlines():
    l = line.strip().split('\t')
    book_id_to_num[l[1] ] = l[0]
    book_id_to_tag_str[l[1] ] = l[2]

sql = "SELECT user_id,count(*) AS c FROM book_comments GROUP BY user_id HAVING  c  > 5 ORDER BY c DESC"
tag_dict = {}

bb = set()
fo = codecs.open('data.txt', 'w', encoding='utf-8')
try:
    cursor.execute(sql)
    results = cursor.fetchall()
    bidset =  set()

    user_to_count = {}
    utc_index = 0

    for row in results:
        bidset.add(row[0])
        user_to_count[row[0]] = str(utc_index)
        utc_index = utc_index + 1
    ll = list(bidset)

    for i in range(len(ll)): # 遍历活跃用户
        sql2 = "SELECT * FROM book_comments WHERE user_id = %s"%ll[i]
        cursor.execute(sql2)
        rrr = cursor.fetchall()

        for o in rrr:
            bb.add(o[2])
            if user_id_to_num.get(o[2],-1) == -1:
                user_id_to_num[o[2]] = user_id_to_num_index
                user_id_to_num_index = user_id_to_num_index + 1
            fo.write(str(user_id_to_num[o[2]]) + '\t')
            fo.write(str(book_id_to_num[o[3]]) + '\t')

            f = (o[5] - datetime(1970, 1, 1)).total_seconds()
            timestrap = str(int(f)) + '000'
            fo.write(timestrap)
            fo.write('\t')

            fo.write()

            fo.write(str(book_id_to_tag_str[o[3]]) + '\t')
            fo.write(str(book_id_to_tag_str[o[3]]) + '\t')

            fo.write(o[4] + '\n')

    bb = list(bb)
    for z in range(len(bb)):
        pass

except Exception as e:
    print str(e)

