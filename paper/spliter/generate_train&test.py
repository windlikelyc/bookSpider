import codecs
import random

fo = codecs.open('data.txt', 'r', encoding='utf-8')
ftr = codecs.open('train.txt', 'w', encoding='utf-8')
fte = codecs.open('test.txt', 'w', encoding='utf-8')

usertr = set()

for line in fo.readlines():
    r = random.randint(0,4)
    if r == 3 and line.split("\t")[0] in usertr:
        fte.write(line)
    else:
        ftr.write(line)
        usertr.add(line.split("\t")[0])
fte.flush()
ftr.flush()
fo.close()
fte.close()
ftr.close()
