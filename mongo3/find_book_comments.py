# encoding:utf-8
# 查看一本书有多少评论
# 用户采用数据集中所有评论数目大于50本书的，调用API，用户有多个标签用逗号隔开

# num : 想要的用户数量
# 1078790 10月31日 图书id 编号到这里

import json
import urllib2

import pymysql
from DBUtils.PooledDB import PooledDB
import time

insert_to_mysql = True
num_of_api = 0

def get_books(num,offset=0):
    list_want = list()
    i = 1
    j = 1
    with open('books.dat', 'r') as f:
        for line in f.readlines():
            if j > offset:
                list_want.append(line.strip())
                i = i + 1
            j = j + 1
            if i > num:
                break
    return list_want

def connet_to_mysql(sql_list): #将一大堆sql语句插入到数据库中
    conn = pymysql.connect(host='39.106.39.216',
                                user='root',
                                passwd="admin123",
                                db='doubandb_test',
                                port=3306,
                                charset='utf8')
    return conn

# 将一个dict转换为
def get_para(item):
    now = int(round(time.time() * 1000))
    now02 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(now / 1000))
    return '("%s","%s","%s","%s","%s","%s","%s","%s")'%(item['votes'],item['user_id'],item['book_id'],item['rating'],item['published'],item['alt'],item['summary'],now02)

def get_html(bid,start,count):
    global num_of_api
    num_of_api = num_of_api + 1
    url = "https://api.douban.com/v2/book/%s/comments?apikey=0b2bdeda43b5688921839c8ecb20399b&start=%s&count=%s"%(bid,start,count)
    try:
        response = urllib2.urlopen(url)
    except Exception as e:
        print  e
        return None
    return json.loads(response.read())

# 返回uid的c条 有效 评论
def get_user_collections(uid,wanted_count,min_count = 2,max_count = 100,strict_comment=True,strict_rating=True,strict_tag = True):

    records = []
    un = open('book_unvalid.dat', 'a') # 记录没有评论的用户
    comments_count = 0
    html = get_html(uid,0,100) # 先试试水
    if html is None:
        return [],0

    already = 0
    cycle = 0
    if html['total'] >= min_count :
        comments_count = html['total']
        num = min(100,html['total'])
        for i in range(num):
            try:
                tmp = dict()
                term = html['comments'][i]
                if int(term['votes']) == 0:
                    continue
                tmp['published'] = term['published']
                tmp['votes'] = term['votes']

                if strict_rating :
                    tmp['rating'] = term['rating']['value']
                else :
                    if term.get('rating','0') == '0':
                        tmp['rating'] = ''
                    else:
                        tmp['rating'] = term['rating']['value']
                if strict_comment :
                    tmp['summary'] = term['summary']
                else:
                    tmp['summary'] = term.get('summary','')
                tmp['book_id'] = uid
                tmp['user_id'] = term['author']['id']
                tmp['alt'] = term['alt']
                records.append(tmp)
                already = already + 1
            except Exception as e:
                pass
        while already < wanted_count and cycle < html['total'] / 100:
            cycle = cycle + 1
            html = get_html(uid,cycle*100,100)
            num = min(100, html['total'] - cycle * 100)
            for i in range(num):
                try:
                    tmp = dict()
                    term = html['comments'][i]
                    if int(term['votes']) == 0:
                        continue
                    tmp['published'] = term['published']
                    tmp['votes'] = term['votes']

                    if strict_rating:
                        tmp['rating'] = term['rating']['value']
                    else:
                        if term.get('rating', '0') == '0':
                            tmp['rating'] = ''
                        else:
                            tmp['rating'] = term['rating']['value']
                    if strict_comment:
                        tmp['summary'] = term['summary']
                    else:
                        tmp['summary'] = term.get('summary', '')
                    tmp['book_id'] = uid
                    tmp['user_id'] = term['author']['id']
                    tmp['alt'] = term['alt']
                    records.append(tmp)
                    already = already + 1
                except Exception as e:
                    pass
    else:
        un.write(uid)
        un.write('\n')
        un.flush()
    if len(records) < wanted_count:
        records = []
    return records,comments_count
if __name__ == "__main__":
    list = get_books(80000,offset=16162)
    if insert_to_mysql:
        # conn = pymysql.connect(host='39.106.39.216',
        #                        user='root',
        #                        passwd="admin123",
        #                        db='doubandb_test',
        #                        port=3306,
        #                        charset='utf8')
        # cursor = conn.cursor()
        pool = PooledDB(pymysql,5,host='39.106.39.216',
                        user='root',
                        passwd="admin123",
                        db='doubandb_test',
                        port=3306,
                        charset='utf8')



    log = open('log', 'a')
    for i in range(len(list)):
        global num_of_api
        if num_of_api > 9500:
            num_of_api = 0
            time.sleep(2*60*60)

        per_user = get_user_collections(list[i],wanted_count=2,strict_comment=False,strict_rating=True)
        sql_list = []
        for j in range(len(per_user[0])):
            try:

                sql = 'Insert into book_comments_new (votes,user_id,book_id,rating,published,alt,summary,create_time) VALUES ' + get_para(per_user[0][j])
                if insert_to_mysql:
                    conn = pool.connection()
                    cur = conn.cursor()
                    cur.execute(sql)
                    conn.commit()

                    # cursor.execute(sql)
                    # conn.commit()
            except Exception as e:
                now = int(round(time.time() * 1000))
                now02 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(now / 1000))
                log.write(now02)
                log.write('\t')
                log.write(str(e))
                log.write('\n')
                log.flush()
            finally:
                cur.close()
                conn.close()







