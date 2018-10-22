# encoding:utf-8
import pymongo

import requests
import json
import time
import urllib2

listWant = list()
listAlr = list()

client = pymongo.MongoClient(host='localhost',port=27017)
db = client.doubandb
collection = db.comments

with open('wanted', 'r') as f:
    for line in f.readlines():
        listWant.append(line.strip())

with open('already','r') as f:
    for line in f.readlines():
        listAlr.append(line.strip())

bookIdList = list(set(listWant).difference(set(listAlr)))
count = len(bookIdList) -1
url = "https://api.douban.com/v2/book/"
url2 = "/comments?apikey=0b2bdeda43b5688921839c8ecb20399b&count=100"
f = open('already','a')
log = open('log','a')
index = 1
while index < count:
    try:
        if index % 9950 == 0:
            time.sleep(24*60*60) # 睡一整天
        tmp = url + bookIdList[index] + url2
        response = urllib2.urlopen(tmp)
        html = json.loads(response.read())
        if html['total'] > 0:
            collection.insert(html)
        f.write(bookIdList[index])
        f.write('\n')
        f.flush()
    except Exception as e:
        now = int(round(time.time() * 1000))
        now02 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(now / 1000))
        log.write(now02 + str(e)+' ')
        log.write(bookIdList[index]+'写入失败')
        log.write('\n')
        log.flush()
    finally:
        index = index + 1
f.close()
log.close()


