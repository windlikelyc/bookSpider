# encoding:utf-8
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import codecs
import warnings
import functools
from collections import Counter

# 统计出版社数量 返回格式:[1,5,7,8,3,5...] 出版社的数量
def get_publisher_count_list(user_id,undupcate=False):
    fo = codecs.open('input.data', 'r', encoding='utf-8')
    y_test = []
    publisher_count = {}

    if undupcate:
        dup = set()

    for line in fo.readlines():
        seq = line.split("\t")
        if seq[0] == user_id:

            if undupcate:
                list = []
                list.append(line.split('\t')[-4])
                list.append(line.split('\t')[-3])
                list = tuple(list)
                if list in dup:
                    continue
                else:
                    dup.add(list)


            publisher_count[seq[-3]] = publisher_count.get(seq[-3], 0) + 1
    for v in publisher_count.values():
        y_test.append(v)
    fo.close()
    return y_test


def get_author_count_list(user_id,undupcate=False):
    y_test = []
    if undupcate:
        dup = set()

    with codecs.open('input.data', 'r', encoding='utf-8') as fo:
        author_count = {}
        for line in fo.readlines():
            if line.split('\t')[0] == user_id:

                if undupcate:

                    list = []
                    list.append(line.split('\t')[-4])
                    list.append(line.split('\t')[-3])
                    list = tuple(list)
                    if list in dup:
                        continue
                    else:
                        dup.add(list)

                seq = line.split('\t')[-4].split('.')
                for v in seq:
                    author_count[v] = author_count.get(v, 0) + 1
    for v in author_count.values():
        y_test.append(v)

    print Counter(y_test)

    # for key, value in sorted(author_count.iteritems(), key=lambda (k, v): (v,k),reverse=True):
    #     print "%s,%s" % (key,value)

    return y_test


def get_publisher_count_dict(user_id):
    di = {}
    with codecs.open('input.data', 'r', encoding='utf-8') as fo:
        author_count = {}
        for line in fo.readlines():
            if line.split('\t')[0] == user_id:
                seq = line.split('\t')[-3].split('.')
                for v in seq:
                    author_count[v] = author_count.get(v, 0) + 1
    for k,v in author_count.items():
        di[k] = v
    return di


def print_max_count_users():
    user_count = {}
    fo = codecs.open('input.data', 'r', encoding='utf-8')
    for line in fo.readlines():
        seq = line.split("\t")
        user_count[seq[0]] = user_count.get(seq[0], 0) + 1
    for key, value in sorted(user_count.iteritems(),
                             key=lambda (k, v): (v, k), reverse=True):
        print "%s:%s" % (key, value)


def draw_plot(y_test):
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.plot([i for i in range(len(y_test))], y_test, 'black', label='Author Preferrence')  # a
    # ax.scatter([i for i in range(len(y_test))],y_test, label='Traning Data') #scatter 代表散点图
    ax.legend(loc=2)
    plt.show()

def draw_hist(y_test):
    # 设置matplotlib正常显示中文和负号
    matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 用黑体显示中文
    matplotlib.rcParams['axes.unicode_minus'] = False  # 正常显示负号
    # 随机生成（10000,）服从正态分布的数据
    # data = np.random.randn(10000)
    data = y_test
    """
    绘制直方图
    data:必选参数，绘图数据
    bins:直方图的长条形数目，可选项，默认为10
    normed:是否将得到的直方图向量归一化，可选项，默认为0，代表不归一化，显示频数。normed=1，表示归一化，显示频率。
    facecolor:长条形的颜色
    edgecolor:长条形边框的颜色
    alpha:透明度
    """
    plt.hist(data, bins=40, normed=0, facecolor="blue", edgecolor="black", alpha=0.7)
    # 显示横轴标签
    plt.xlabel("X axis")
    # 显示纵轴标签
    plt.ylabel("Y axis")
    # 显示图标题
    plt.title("The distribution of Reading")
    plt.show()


def draw_bar(y_test):
    matplotlib.rcParams['font.sans-serif'] = ['SimHei']
    matplotlib.rcParams['axes.unicode_minus'] = False

    label_list = ['2014', '2015', '2016', '2017']  # 横坐标刻度显示值
    num_list1 = [20, 30, 15, 35]  # 纵坐标值1
    num_list2 = [15, 30, 40, 20]  # 纵坐标值2
    x = range(len(num_list1))
    """
    绘制条形图
    left:长条形中点横坐标
    height:长条形高度
    width:长条形宽度，默认值0.8
    label:为后面设置legend准备
    """
    rects1 = plt.bar(left=x, height=num_list1, width=0.4, alpha=0.8, color='red', label="aaaa")
    rects2 = plt.bar(left=[i + 0.4 for i in x], height=num_list2, width=0.4, color='green', label="bbbb")
    plt.ylim(0, 50)  # y轴取值范围
    plt.ylabel("142")
    """
    设置x轴刻度显示值
    参数一：中点坐标
    参数二：显示值
    """
    plt.xticks([index + 0.2 for index in x], label_list)
    plt.xlabel("132")
    plt.title("123")
    plt.legend()  # 设置题注
    # 编辑文本
    for rect in rects1:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2, height + 1, str(height), ha="center", va="bottom")
    for rect in rects2:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2, height + 1, str(height), ha="center", va="bottom")
    plt.show()


def get_time_distribution():
    return [0.12946428571428573
,0.11160714285714286
,0.14732142857142858
,0.11160714285714286
,0.11160714285714286
,0.12946428571428573
,0.11160714285714286
,0.14732142857142858]

if __name__ == '__main__':
    # draw_hist(get_time_distribution())
    draw_bar(None)



'''
2802
9855
打印活跃用户
9724:663
20328:620
15532:482
9661:359
2802:324
14764:300
8139:272
8713:261
15214:258
17477:251
4354:250
20393:243
25744:239
7899:236
7887:236
9855:232
17398:217
25703:211
9916:200
7738:199
19334:189
'''
