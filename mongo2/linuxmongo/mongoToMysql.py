# encoding:utf-8
# 将mongodb的数据导入到数据库中

import pymongo


listWant = list()
listAlr = list()

client = pymongo.MongoClient(host='39.106.39.216',port=27017)
db = client.doubandb
collection = db.comments

results = collection.find()
for result in results:
    print(result)


