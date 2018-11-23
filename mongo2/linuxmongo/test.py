# encoding:utf-8
# 查看用户有多少个评论
import pymongo



listWant = list()
listAlr = list()

client = pymongo.MongoClient(host='39.106.39.216',port=27017)
db = client.doubandb
collection = db.students

results = collection.find().count()
print(results)


