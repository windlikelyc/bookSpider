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

user_id = ['liuyaochen','zhangsan','lisi','wangwu']
book_id = ['213','547','215','2151']
tags=['荷花','荷花','荷花','荷花']
updated=['2018-09-25 13:30:21','2018-09-25 13:30:21','2018-09-25 13:30:21','2018-09-25 13:30:21']

sql = "SELECT * FROM user_collections"
tag_dict = {}
fo = codecs.open('data.txt', 'w', encoding='utf-8')


try:
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        uid = row[2]
        bid = row[3]
        time = row[5]
        tags = row[6].split(',')
        for i in range(len(tags)):
            tag_dict[tags[i]] = tag_dict.get(tags[i] , 0) + 1
    biaohao = 0

    valid_tags = {} # key 有效标签，value 标号
    valid_u_dict = {} # key 有用户，value 标号
    valid_b_dict = {} # key 有标签，value 标号

    list_top_tags = sorted(tag_dict.items(), key=lambda d: d[1], reverse=True)
    for i in range(len(list_top_tags)):
        if list_top_tags[i][1] > 30:
            if valid_tags.get(list_top_tags[i][0] , -1) == -1:
                valid_tags[list_top_tags[i][0]] = biaohao
                biaohao = biaohao + 1

    print "有效标签数量" , len(valid_tags)

    cursor.execute(sql)
    results = cursor.fetchall()
    valid_records = 0
    valid_book_id = {}
    valid_user_id = {}
    uidbiaohao = 0
    bidbiaohao = 0
    for row in results:
        tags = row[6].split(',')
        max_count = 0
        tmp_tg=[]
        if valid_user_id.get(row[2],-1) == -1:
            valid_user_id[row[2]] = uidbiaohao
            uidbiaohao = uidbiaohao + 1
        if valid_book_id.get(row[3],-1) == -1:
            valid_book_id[row[3]] = bidbiaohao
            bidbiaohao = bidbiaohao + 1

        # valid_user_id.add(row[2])
        for i in range(len(tags)):
            if tag_dict.get(tags[i]) > 30:
                tmp_tg.append(tags[i])
        if len(tmp_tg) > 0:
            valid_records = valid_records + 1

            fo.write(str(valid_user_id[row[2]])+'\t')
            fo.write(str(valid_book_id[row[3]])+'\t')
            f = (row[5] - datetime(1970, 1, 1)).total_seconds()
            sss = str(int(f)) + '000'
            fo.write(sss)
            fo.write('\t')
            fo.write('.'.join(map(lambda x: str(valid_tags[x]),tmp_tg))+'\t')
            fo.write('.'.join(map(lambda x: str(valid_tags[x]), tmp_tg)) + '\t')
            fo.write('40.3967441'+'\t')
            fo.write('-80.0847998'+'\t')
            fo.write('19.52.76.32.33.34.35.36.77.2.21.3.75.68'+'\t')
            fo.write('1'+'\t')
            fo.write('4'+'\t')
            fo.write('-1'+'\t')
            fo.write('0'+'\n')
        else:
            valid_book_id.pop(row[3],None)
            valid_user_id.pop(row[2],None)
            bidbiaohao = bidbiaohao - 1
            uidbiaohao = uidbiaohao - 1
    print "至少打了一个有效标签的图书总数为" , valid_records
    print "至少打了一个有效标签的用户的图书总数为" , len(valid_book_id)
    print "至少打了一个有效标签的用户的用户总数为" , len(valid_user_id)


except Exception as e:
    print str(e)
fo.flush()
fo.close()
print "总的标签数量为",len(tag_dict)

# with open('data.txt', 'w') as f:
#     for i in range(len(user_id)):
#         f.write(user_id[i]+'\t')
#         f.write(book_id[i]+'\t')
#         f.write(tags[i]+'\t')
#         f.write(updated[i]+'\n')

