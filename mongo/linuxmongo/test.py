# encoding:utf-8
import codecs
import json
import urllib2

import pymongo


listWant = list()
listAlr = list()

client = pymongo.MongoClient(host='39.106.39.216',port=27017)
db = client.doubandb
collection = db.students



fo = codecs.open('data.txt', 'r', encoding='utf-8')
book_ids =[]
book_t0_num = {}
btnint = 0

for line in fo.readlines():
    book_ids.append(line.strip())
    book_t0_num[line.strip()] = str(btnint)
    btnint = btnint + 1

fo.close()

fo2 = codecs.open('book_id_map.txt', 'w', encoding='utf-8')

tag_dict = {}  # tag名称-- 对应序号

book_tag = {}  # book_id -- 对应一个list['tagname']

numgerator = 0
for i in range(len(book_ids)):
    results = collection.find_one({'id':book_ids[i]})
    if results is None:
        url = "https://api.douban.com/v2/book/%s?apikey=0b2bdeda43b5688921839c8ecb20399b" % (book_ids[i])
        try:
            response = urllib2.urlopen(url)
            print '开一个请求',book_ids[i]
        except Exception as e:
            print  e
        results = json.loads(response.read())
    if results is None:
        continue
    wondertag = min(2, len(results['tags']))
    if wondertag == 0:
        continue
    book_tag[book_ids[i]] = []

    for j in range(wondertag):
        if tag_dict.get(results['tags'][j]['name'], -1) == -1:
            tag_dict[results['tags'][j]['name']] = numgerator
            book_tag[book_ids[i]].append(numgerator)
            numgerator = numgerator + 1
        else:
            book_tag[book_ids[i]].append(tag_dict[results['tags'][j]['name']])
    fo2.write(book_t0_num[book_ids[i]])
    fo2.write('\t')
    fo2.write(book_ids[i])
    fo2.write('\t')
    book_tag[book_ids[i]] = map(str,book_tag[book_ids[i]])
    if len(book_tag[book_ids[i]]) == 0:
        print "wrong",book_ids[i]
        raise RuntimeError('testError')

    fo2.write(".".join(book_tag[book_ids[i]]))
    fo2.write('\n')
    fo2.flush()


print(book_tag)


