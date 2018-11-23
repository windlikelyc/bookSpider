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

fo = codecs.open('data2.txt','r',encoding='utf-8')
fo_write = codecs.open('data_convertor.txt', 'w', encoding='utf-8')

# 初始化
seq_user = {}
seq_book = {}

seqU = 1
seqB = 1

seqT = 1
seqP = 1



for line in fo.readlines():
    seq = line.strip().split("\t")

    if seq[0] not in seq_user:
        seq_user[seq[0]] = seqU
        seqU = seqU + 1

    if seq[1] not in seq_book:
        seq_book[seq[1]] = seqB
        seqB = seqB + 1




fo.seek(0)

for line in fo.readlines():
    seq = line.strip().split("\t")

    fo_write.write(str(seq_user[seq[0]]))
    fo_write.write("\t")

    fo_write.write(str(seq_book[seq[1]]))
    fo_write.write("\t")

    fo_write.write(seq[-1])
    fo_write.write("\n")




