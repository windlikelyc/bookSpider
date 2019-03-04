import codecs

fo_write = codecs.open('output.txt', 'w', encoding='utf-8')

fo = codecs.open('data.txt','r',encoding='utf-8')

for line in fo.readlines():
    seq = line.strip().split("\t")

    fo_write.write(seq[0] + '\t' + seq[1] + '\t' + seq[-1] + '\n')

fo_write.flush()
