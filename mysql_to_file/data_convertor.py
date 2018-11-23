# -*- coding: UTF-8 -*-
# 一个数据转换器，将  图书 - 用户 - 出版🐍 - 作者标签映射到 seq 模式
'''
    主要思路
    list = []
    if id not in  list
        list.append(id)

    print list.index(id)

'''
import codecs

fo = codecs.open('data.txt','r',encoding='utf-8')
fo_write = codecs.open('data_convertor.txt', 'w', encoding='utf-8')

# 初始化
seq_user = []
seq_book = []
seq_tags = []
seq_author = []
seq_publisher = []


for line in fo.readlines():
    seq = line.strip().split("\t")

    if seq[0] not in seq_user:
        seq_user.append(seq[0])

    if seq[1] not in seq_book:
        seq_book.append(seq[1])

    tags = seq[3].split(".")
    for t in range(len(tags)):
        if tags[t] not in seq_tags:
            seq_tags.append(tags[t])

    authors = seq[4].split(".")
    for a in range(len(authors)):
        if authors[a] not in seq_author:
            seq_author.append(authors[a])

    if seq[5] not in seq_publisher:
        seq_publisher.append(seq[5])

fo.seek(0)

for line in fo.readlines():
    seq = line.strip().split("\t")

    fo_write.write(str(seq_user.index(seq[0])))
    fo_write.write("\t")

    fo_write.write(str(seq_book.index(seq[1])))
    fo_write.write("\t")

    fo_write.write(seq[2])
    fo_write.write("\t")

    ta_l = []
    tags = seq[3].split(".")
    for t in range(len(tags)):
        ta_l.append(seq_tags.index(tags[t]))
    fo_write.write(".".join(map(str,ta_l)))
    fo_write.write("\t")

    au_l = []
    authors = seq[4].split(".")
    for a in range(len(authors)):
        au_l.append(seq_author.index(authors[a]))
    fo_write.write(".".join(map(str,au_l)))
    fo_write.write("\t")

    fo_write.write(str(seq_publisher.index(seq[5])))
    fo_write.write("\t")

    fo_write.write(seq[6])
    fo_write.write("\n")




