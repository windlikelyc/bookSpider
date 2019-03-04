
#!/usr/bin/python
# -*- coding: UTF-8 -*-
# generate userid bookid time tag publisher rate

# acordding to the result , the spasibility is to sparse,about 0.00000119545

import pymysql
import codecs

from datetime import datetime

class MyErr(Exception):
    pass

conn = pymysql.connect(host='39.106.39.216',
                       user='root',
                       passwd="admin123",
                       db='doubandb_test',
                       port=3306,
                       charset='utf8')

cursor = conn.cursor()
sql_find_tag_of_user = "SELECT user_id,book_id,tags FROM `user_collections_1`;"

user_set = set()
book_set = set()
tag_set = set()


try:
    cursor.execute(sql_find_tag_of_user)
    results = cursor.fetchall()
    for row in results:
        user_set.add(row[0])
        book_set.add(row[1])
        for t in row[-1].split(","):
            for tt in t.split("/"):
                tag_set.add(tt)
except Exception as e:
        print e

print 'users' + str(len(user_set))
print 'books' + str(len(book_set))
print 'tags' + str(len(tag_set))

output_file_name = 'all_tags.txt'
fo_write = codecs.open(output_file_name , 'w', encoding='utf-8')

i = 0
for t in tag_set:
    fo_write.write(t)
    if i < 10:
        i = i + 1
        fo_write.write('\t')
    else:
        i = 0
        fo_write.write('\n')









