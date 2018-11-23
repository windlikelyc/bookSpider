# -*- coding: UTF-8 -*-
# 一个数据转换器，将  图书 - 用户 - 出版🐍 - 作者标签映射到 seq 模式
# 首先将　完整的数据　放到input 中，格式如下
#   1941752	1892695	1259971200000	随笔.散文	洁尘	东方出版中心	4
# 1941752	3402881	1259539200000	睡眠.健康	(英)查里斯•艾德茨考斯基	北方文艺	3
# 1941752	3628749	1347235200000	向世界呼喊吧.BIGBNAG	bigbang.金世儿 整理	NoPub	5
# 运行文件，输出到output.txt

# 注意：有时候可能会有数据修改什么的，重新生成编号！
import codecs

fo = codecs.open('input.data','r',encoding='utf-8')
fo_write = codecs.open('output.data', 'w', encoding='utf-8')

# 初始化
seq_user = {}
seq_book = {}
seq_tag = {}
seq_au = {}
seq_pub = {}


seqU = 1
seqB = 1

seqT = 1
seqA = 1
seqP = 1



for line in fo.readlines():
    seq = line.strip().split("\t")

    if seq[0] not in seq_user:
        seq_user[seq[0]] = seqU
        seqU = seqU + 1

    if seq[1] not in seq_book:
        seq_book[seq[1]] = seqB
        seqB = seqB + 1

    tags = seq[3].split(".")
    for t in range(len(tags)):
        if tags[t] not in seq_tag:
            seq_tag[tags[t]] = seqT
            seqT = seqT + 1

    aus = seq[4].split(".")
    for t in range(len(aus)):
        if aus[t] not in seq_au:
            seq_au[aus[t]] = seqA
            seqA = seqA + 1

    if seq[5] not in seq_pub:
        seq_pub[seq[5]] = seqP
        seqP = seqP + 1

fo.seek(0)

for line in fo.readlines():
    seq = line.strip().split("\t")

    fo_write.write(str(seq_user[seq[0]]))
    fo_write.write("\t")

    fo_write.write(str(seq_book[seq[1]]))
    fo_write.write("\t")

    fo_write.write(str(seq[2]))
    fo_write.write("\t")


    ta_l = []
    tags = seq[3].split(".")
    for t in range(len(tags)):
        ta_l.append(seq_tag[tags[t]])
    fo_write.write(".".join(map(str, ta_l)))
    fo_write.write("\t")

    au_l = []
    authors = seq[4].split(".")
    for a in range(len(authors)):
        au_l.append(seq_au[authors[a]])
    fo_write.write(".".join(map(str, au_l)))
    fo_write.write("\t")


    fo_write.write(str(seq_pub[seq[5]]))
    fo_write.write("\t")

    fo_write.write(str(seq[-1]))
    fo_write.write("\t")



    fo_write.write(seq[-1])
    fo_write.write("\n")




