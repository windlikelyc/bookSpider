# -*- coding: UTF-8 -*-
import codecs

import pymysql
import time
import random
from datetime import datetime, timedelta

fo = codecs.open('data.txt','r',encoding='utf-8')

book_dict={}
user_dict={}

valid_book = set()

user_id = set()

for line in fo.readlines():
    try:
        seq = line.strip().split("\t")

        if book_dict.get(seq[1],-1) == -1:
            book_dict[seq[1]] = []
            book_dict[seq[1]].append(seq[0])
        else:
            book_dict[seq[1]].append(seq[0])

    except Exception as e:
        print e


count = 0
for a in book_dict:
    if len(book_dict[a]) >= 2:
        valid_book.add(a)
        count = count + 1


fo2 = codecs.open('data3.txt', 'w', encoding='utf-8')

fo.seek(0)

# for line in fo.readlines():
#     try:
#         seq = line.strip().split("\t")
#         if seq[1] in valid_book:
#             fo2.write(line)

    # except Exception as e:
    #     print e

valid_book_list = list(valid_book)
valid_book_list.sort()
for i in valid_book_list:
    fo2.write(i)
    fo2.write('\n')



print count