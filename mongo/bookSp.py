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
collection = db.students

with open('wanted', 'r') as f:
    for line in f.readlines():
        listWant.append(line.strip())

with open('already','r') as f:
    for line in f.readlines():
        listAlr.append(line.strip())

bookIdList = list(set(listWant).difference(set(listAlr)))

count = len(bookIdList) -1

url = "https://api.douban.com/v2/book/"

f = open('already','a')
log = open('log','a')

sleeptime = 10



while count != -1:
    try:
        tmp = url + bookIdList[count]
        response = urllib2.urlopen(tmp)
        html = json.loads(response.read())
        collection.insert(html)

        f.write(bookIdList[count])
        f.write('\n')
        f.flush()
        print bookIdList[count] + "已写入\n"
        count = count -1
    except Exception as e:
        now = int(round(time.time() * 1000))
        now02 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(now / 1000))
        log.write(now02 + str(e)+' ')
        log.write(bookIdList[count]+'写入失败')
        log.write('\n')
        log.flush()
        count = count -1
    finally:
        time.sleep(60)

f.close()
log.close()


