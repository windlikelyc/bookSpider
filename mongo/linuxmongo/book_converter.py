# encoding:utf-8
# 输入：图书isbn
# 输出：图书对应的序列号，标签，作者，出版社
# 使用方式，将想要爬去的图书id放到data 文件中， 输出的文件就会在book——id——map中，之后可以联系用户评论进一步做转化。

# 本脚本过滤掉了所有标签和作者 完 全 一 致 的标签，因为作者信息已经很能够表现图书主题了
import codecs
import json
import urllib2
import string
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

book_author = {} # book_id -- 对应str 作者

book_publisher = {} # book_id -- 对用 str 出版社

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
    wondertag = min(2, len(results['tags'])) # 卡两个标签，多了不要



    if wondertag == 0:
        continue
    book_tag[book_ids[i]] = []
    book_author[book_ids[i]] = []

    book_publisher[book_ids[i]] = results['publisher']

    already_tag_count = 0 # 过滤掉作者标签
    while wondertag > 0:
        if already_tag_count >= len(results['tags']):
            break
        wtg = results['tags'][already_tag_count]['name']
        if len(results['author']) > 0:
            if string.find(results['author'][0] ,wtg) != -1 or string.find(wtg,results['author'][0] ) != -1:
                already_tag_count = already_tag_count + 1
                continue
        book_tag[book_ids[i]].append(results['tags'][already_tag_count]['name'])
        already_tag_count = already_tag_count + 1
        wondertag = wondertag - 1

    for j in range(wondertag):
        book_tag[book_ids[i]].append(results['tags'][j]['name'])

    for j in range(len(results['author'])):
        book_author[book_ids[i]].append(results['author'][j])


    fo2.write(book_t0_num[book_ids[i]])
    fo2.write('\t')
    fo2.write(book_ids[i])
    fo2.write('\t')
    fo2.write(".".join(book_tag[book_ids[i]]))
    fo2.write('\t')

    if len(book_author[book_ids[i]]) == 0:
        fo2.write(u"None")
    else:
        fo2.write(".".join(book_author[book_ids[i]]))

    fo2.write("\t")
    fo2.write(book_publisher[book_ids[i]])
    fo2.write("\n")

    fo2.flush()




