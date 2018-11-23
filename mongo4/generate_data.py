# -*- coding: UTF-8 -*-
# 标签数量总共有7078 个，但是出现次数大于 x 次的有 y 个（30，175），（20，261），（10，486）
import codecs

import pymysql
import time
import random
from datetime import datetime, timedelta
# 生成 用户--图书--评分，没有用到 序号
conn = pymysql.connect(host='39.106.39.216',
                       user='root',
                       passwd="admin123",
                       db='doubandb_test',
                       port=3306,
                       charset='utf8')
cursor = conn.cursor()

# fo = codecs.open('book_id_map.txt','r',encoding='utf-8')

# 生成 图书的字典
# book_dict = {}
#
# for line in fo.readlines():
#     try:
#         seq = line.strip().split("\t")
#         author_and_pub = [seq[2],seq[3],seq[4]]
#         book_dict[seq[1]] = author_and_pub
#     except Exception as e:
#         print e


# fo.close()

sql = "SELECT user_id,count(*) AS c FROM book_comments_new GROUP BY user_id HAVING  c  > 1 ORDER BY c DESC"
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
    ll = list(bidset) # ll 是活跃用户

    for i in range(len(ll)): # 遍历活跃用户
        sql2 = "SELECT * FROM book_comments_new WHERE user_id = %s"%ll[i]
        cursor.execute(sql2)
        rrr = cursor.fetchall()

        for o in rrr:

            fo.write(o[2] + '\t')
            fo.write(o[3] + '\t')

            f = (o[5] - datetime(1970, 1, 1)).total_seconds()
            timestrap = str(int(f)) + '000'
            fo.write(timestrap)
            fo.write('\t')

            # fo.write(book_dict[o[3]][0])
            # fo.write('\t')
            # fo.write(book_dict[o[3]][1])
            # fo.write('\t')
            # fo.write(book_dict[o[3]][2])
            # fo.write('\t')

            fo.write(o[4] + '\n')

except Exception as e:
    print str(e)

