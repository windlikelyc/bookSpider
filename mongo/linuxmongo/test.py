# encoding:utf-8
import pymongo


listWant = list()
listAlr = list()

client = pymongo.MongoClient(host='39.106.39.216',port=27017)
db = client.doubandb
collection = db.students

results = collection.find().count()
print(results)


