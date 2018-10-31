import codecs
import random

fo = codecs.open('data.txt', 'r', encoding='utf-8')
ftr = codecs.open('train.txt', 'w', encoding='utf-8')
fte = codecs.open('test.txt', 'w', encoding='utf-8')


for line in fo.readlines():
    r = random.randint(0,4)
    if r == 3:
        fte.write(line)
    else:
        ftr.write(line)
fte.flush()
ftr.flush()
fo.close()
fte.close()
ftr.close()
