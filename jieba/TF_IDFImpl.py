
#encoding=utf-8
import numpy as np
import os   #用于打开一个文件，并遍历文件中所有的txt文件，存储到数组中
import jieba  #结巴分词
import io
import numpy as np
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

filePath = "E:/spider/booksummery/"  #txt文本集所在的文件夹路径
txtNames = list()                     #所有txt文档名字
result_array = list()

def oneWork():  #把文档中的所有文件名字存入数组

    pathDir = os.listdir(filePath) #把等前文件夹里的所有txt文档的名字都获取了，放入数组
    for allDir in pathDir:
        if(allDir.find('txt') >= 0 and allDir.find('result') < 0):
            txtNames.append(allDir)
            #print('txtName one =', allDir)
    return

def fenciWork():

    for f in txtNames:
        #print('texName=', f)
        basePath = '%s%s' % (filePath, f) #拼接为单个文档的绝对路径
        #print('basePath=', basePath)

        fr = io.open(basePath, mode='r+', encoding='utf-8')
        s = fr.read()             #读取文档的文章
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
        # print('result_array=', result_array)
        fr.close()
    return result_array

def IDFWork():

    vectorizer = CountVectorizer()
    transformer = TfidfTransformer()
    vetzer = vectorizer.fit_transform(fenciWork()) #计算每个词在每个文档中的词频
    vetzer_array = vetzer.toarray() #把词频转为词频矩阵存入数组
    feature_array = vectorizer.get_feature_names()  #词频矩阵，每一行每个元素对应的 词的值
    print('vetzer=', vetzer_array.shape, 'names', len(feature_array))

    result = transformer.fit_transform(vetzer.toarray()).toarray()

    for (title, w) in zip(feature_array, result[0].tolist()):
        print('title=',title,'w=',w)


    return
def getImportant():
    n = 5  # 前五位


    # for (title, w) in zip(titlelist, weight):
    #     print u'{}:'.format(title)
    #     # 排序
    #     loc = np.argsort(-w)
    #     for i in range(n):
    #         print u'-{}: {} {}'.format(str(i + 1), words[loc[i]], w[loc[i]])
    #     print '\n'

oneWork()
fenciWork()
IDFWork()