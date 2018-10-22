# encoding=utf-8
# 用来加载停用词
import jieba
import io
def stopwordslist(filepath):
    stopwords = [line.strip() for line in io.open(filepath, 'r',encoding="utf-8").readlines()]
    print str(stopwords)
    return stopwords


# 对句子进行分词
def seg_sentence(sentence):
    sentence_seged = jieba.cut(sentence.strip())
    stopwords = stopwordslist('stopwords.txt')  # 这里加载停用词的路径
    outstr = ''
    for word in sentence_seged:
        if word not in stopwords:
            if word != '\t':
                outstr += word
                outstr += " "
    return outstr


if __name__=='__main__':
    inputs = io.open('input.txt', 'r',encoding="utf-8")
    outputs = io.open('output.txt', 'w',encoding="utf-8")
    for line in inputs:
        line_seg = seg_sentence(line)  # 这里的返回值是字符串
        outputs.write(line_seg + '\n')
    outputs.close()
    inputs.close()