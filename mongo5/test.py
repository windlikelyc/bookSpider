# -*- coding: UTF-8 -*-
# 1 首先获得用户－书籍－评分，放到文件1.data 中　包含　164534 条记录
# 2 获得　图书－－作者－－出版社　放到2.data 中 　保函　22441 条记录
# 3 将两者和并，输出到3.data 中
# 4 将data 3 的文件　编号重新排序，生成 用户编号1,2,3...　图书编号1,2,3....


import codecs

fo_1 = codecs.open('1.data','r',encoding='utf-8')
fo_2 = codecs.open('2.data', 'r', encoding='utf-8')
fo_3 = codecs.open('3.data', 'w', encoding='utf-8')

book_dict = {} # key book_id value ['tag','au','pub']
for line in fo_2.readlines():
    seq = line.strip().split("\t")
    author_and_pub = [seq[2],seq[3],seq[4]]
    book_dict[seq[1]] = author_and_pub
fo_2.close()

for line in fo_1.readlines():
    seq = line.strip().split("\t")
    fo_3.write(seq[0])
    fo_3.write("\t")
    fo_3.write(seq[1])
    fo_3.write("\t")
    fo_3.write(seq[2])
    fo_3.write("\t")
    fo_3.write(book_dict[seq[1]][0])
    fo_3.write("\t")
    fo_3.write(book_dict[seq[1]][1])
    fo_3.write("\t")
    fo_3.write(book_dict[seq[1]][2])
    fo_3.write("\t")
    fo_3.write(seq[-1])
    fo_3.write("\n")
fo_3.close()






