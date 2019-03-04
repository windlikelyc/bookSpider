
#!/usr/bin/python
# -*- coding: UTF-8 -*-
# generate userid bookid time tag publisher rate



import pymysql
import codecs

from datetime import datetime

conn = pymysql.connect(host='localhost',
                       user='root',
                       passwd="admin123",
                       db='doubandb',
                       port=3306,
                       charset='utf8')

cursor = conn.cursor()

fo_read = codecs.open('book_id_map.txt','r',encoding='utf-8')

# generate dict of books
book_dict = {}

for line in fo_read.readlines():
    try:
        seq = line.strip().split("\t")
        author_and_pub = [seq[2],seq[3],seq[4]]
        book_dict[seq[1]] = author_and_pub
    except Exception as e:
        print seq[1]
        pass

fo_read.close()


sql = "SELECT user_id,count(*) FROM `book_comments_new` GROUP BY user_id ORDER BY COUNT(*) DESC LIMIT 1439"
active_user_list = [] # the users who votes larger than 20
try:
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        active_user_list.append(row[0])
except:
    print 'error'

output_file_name = 'data.txt'  ################# write output file name there

# fo_write = codecs.open(output_file_name , 'w', encoding='utf-8')


sql_for_user = "SELECT user_id,book_id,rating,published  FROM `book_comments_new` WHERE user_id = "


## seq generator
user_seq = 1
book_seq = 1
tag_seq = 1
autor_seq = 1
publisher_seq = 1


umap = {}
bmap={}
tmap={}
amap={}
pmap={}



tmsql = "SELECT book_id,count(*) FROM `book_comments_new` GROUP BY book_id ORDER BY COUNT(*) DESC  LIMIT 1089 "

active_book_list = [] # the books who voted larger than 15
cursor.execute(tmsql)

results = cursor.fetchall()
for row in results:
    active_book_list.append(row[0])

for uid in active_user_list:
    try:
        cursor.execute(sql_for_user + uid)
        results = cursor.fetchall()

        for row in results:
            if row[1] not in active_book_list : continue

            #  split words and map word to num,then put num to list,finally join list with .
            tags = book_dict[row[1]][0].split(".")
            for t in range(len(tags)):
                if not tmap.has_key(tags[t]):
                    tmap[tags[t]] = tag_seq
                    tag_seq = tag_seq + 1

            ta_l = []
            for t in range(len(tags)):
                ta_l.append(tmap[tags[t]])

            aus = book_dict[row[1]][1].split(".")
            for a in range(len(aus)):
                if  not  amap.has_key(aus[a]):
                    amap[aus[a]] = autor_seq
                    autor_seq = autor_seq + 1

            au_l = []
            for a in range(len(aus)):
                au_l.append(amap[aus[a]])

            if not pmap.has_key(book_dict[row[1]][2]):
                pmap[book_dict[row[1]][2]] = publisher_seq
                publisher_seq = publisher_seq + 1

            if not umap.has_key(row[0]):
                umap[row[0]] = user_seq
                user_seq = user_seq + 1

            if not bmap.has_key(row[1]) :
                bmap[row[1]] = book_seq
                book_seq = book_seq + 1

            f = (row[3] - datetime(1970, 1, 1)).total_seconds()
            timestrap = str(int(f)) + '000'



            # fo_write.write(str(umap[row[0]]) + '\t' + str(bmap[row[1]]) + '\t' + timestrap + '\t' + ".".join(map(str, ta_l) ) + '\t' + ".".join(map(str, au_l) ) + '\t' + str(pmap[book_dict[row[1]][2]]) + '\t' + row[2]  + '\n')
    except  Exception as e:
        print e

# fo_write.flush()
print 'user_seq' + user_seq
print 'book seq' + book_seq
print 'tag_seq' + tag_seq
print 'au_seq' + autor_seq
print 'pu_seq' + publisher_seq