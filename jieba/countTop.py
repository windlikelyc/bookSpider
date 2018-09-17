
#encoding=utf-8
import numpy as np
import os   #用于打开一个文件，并遍历文件中所有的txt文件，存储到数组中
import jieba  #结巴分词
import io
import numpy as np
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer



def titlelist():
    for file in os.listdir('.'):
        if '.' not in file:
            for f in os.listdir(file):
                yield (file + '--' + f.split('.')[0])  # windows下编码问题添加：.decode('gbk', 'ignore').encode('utf-8'))


def wordslist():
    jieba.add_word(u'丹妮莉丝')
    stop_word = [line.strip() for line in io.open("stopwords.txt", 'r',encoding="utf-8").readlines()]
    print len(stop_word)
    for file in os.listdir('.'):
        if '.' not in file:
            for f in os.listdir(file):
                with open(file + '//' + f) as t:
                    content = t.read().strip().replace('\n', '').replace(' ', '').replace('\t', '').replace('\r', '')
                    seg_list = pseg.cut(content)
                    seg_list_after = []
                    # 去停用词
                    for seg in seg_list:
                        if seg.word not in stop_word:
                            seg_list_after.append(seg.word)
                    result = ' '.join(seg_list_after)
                    # wordslist.append(result)
                    yield result


if __name__ == "__main__":

    wordslist = list(wordslist())
    titlelist = list(titlelist())

    vectorizer = CountVectorizer()
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(vectorizer.fit_transform(wordslist))

    words = vectorizer.get_feature_names()  # 所有文本的关键字
    weight = tfidf.toarray()

    print 'ssss'
    n = 5  # 前五位
    for (title, w) in zip(titlelist, weight):
        print u'{}:'.format(title)
        # 排序
        loc = np.argsort(-w)
        for i in range(n):
            print u'-{}: {} {}'.format(str(i + 1), words[loc[i]], w[loc[i]])
        print '\n'