# encoding:utf-8
import numpy as np
import os   #用于打开一个文件，并遍历文件中所有的txt文件，存储到数组中
import jieba  #结巴分词
import io
import numpy as np
import pymysql
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

# 一个大字典，其中key是图书id，value是 一个长度为news_tops 的 词频list
dict = {}
nowid = 0
# 构造dict字典，key是图书id，value是一个dict，其中key是单词，value是词频
di = {}
fo = open("foo.txt", "w")


paraNumber = 100 # 要选取的评论数
topKey = 20 # 关键词个数
cycle = 50 # 文章个数
datas = []
result = None
db = pymysql.connect(host='39.106.39.216', user='root', passwd="admin123", db='doubandb_test', port=3306, charset='utf8',
                     cursorclass=pymysql.cursors.SSDictCursor)
cursor = db.cursor()
sql = 'SELECT * FROM `book_summery` WHERE book_summery != "" and  length(book_summery)>140 LIMIT 100; '
cursor.execute(sql)


# 返回一个由空格隔开的单个的list
def getNextPara():
    return cursor.fetchone()


def fenciWork():
    data = getNextPara()
    s = data['book_summery']
    global nowid
    nowid = data['id']
    dict[nowid] = []
    di[data['id']] = {}

    result_array = list()
    s = s.replace("\n", "")   #去除文章的换行符
    seg_list = jieba.cut(s, cut_all=False)  # 这里是个generator对象
    seg_result = str()        #建立一个空字符串，做后边文字处理后拼接字符使用
    for seg in seg_list:
        if (seg != '' and seg != "\n " and seg != '\n\n'):  # 去除单个文档中文章包含的''、换行、'\n\n'
            seg_result = '%s%s%s' % (seg_result, ' ', seg)

    # for seg in seg_list:
    #     print a
    #     if (seg != '' and seg != "\n " and seg != '\n\n'):  #去除单个文档中文章包含的''、换行、'\n\n'
    #         seg_result = '%s%s%s' % (seg_result, ' ', seg)
    # print('seg_result=', seg_result)
    result_array.append(seg_result)

    folist = list()
    for a in result_array:
        folist.append(a.encode('utf8'))

    fo.write(' '.join(folist))
    fo.write('\n')

    # print('result_array=', result_array)
    return result_array

def IDFWork():
    vectorizer = CountVectorizer()
    transformer = TfidfTransformer()
    vetzer = vectorizer.fit_transform(fenciWork()) #计算每个词在每个文档中的词频
    vetzer_array = vetzer.toarray() #把词频转为词频矩阵存入数组
    feature_array = vectorizer.get_feature_names()  #词频矩阵，每一行每个元素对应的 词的值
    # print('vetzer=', vetzer_array.shape, 'names', len(feature_array))
    result = transformer.fit_transform(vetzer.toarray()).toarray()

    for i in range(len(result[0])):
        di[nowid][feature_array[i]] = vetzer_array[0][i]

    print ('nowid=' , nowid.encode('utf8') , 'dictlen = ' , len(di[nowid]))
    loc = np.argsort(-result[0])
    # print "前20的关键词"
    top = list()
    for i in range(20):
        if len(feature_array) < topKey:
            continue
        top.append(feature_array[loc[i]])
    return top

def getTop():
    return IDFWork()
def calSimilarity(id,id2):
    vector_a = np.mat(id)
    vector_b = np.mat(id2)
    num = float(vector_a * vector_b.T)
    denom = np.linalg.norm(vector_a) * np.linalg.norm(vector_b)
    cos = num / denom
    sim = 0.5 + 0.5 * cos
    return sim




tops = []
for i in range(cycle):
    tops+= getTop()

news_tops = [] # 这个是tfidf算出的关键词列表
for t in tops:
    if t not in news_tops:
        news_tops.append(t)

print ('key wods=' ,news_tops,'len=',len(news_tops))

for i in dict:
    for guanjianci in news_tops:
        dict[i].append(di[i].get(guanjianci,0))
    print ('id=',i,'li=',dict[i])

max = 0
maxId = ''
wonderId = u'1000280'
for i in dict:
    if i == wonderId:
        continue
    a = calSimilarity(dict[i],dict[wonderId])
    if a > max :
        max =a
        maxId = i
print ('the similist boook of',wonderId.encode('utf8'),'is:' ,maxId)
fo.close()







