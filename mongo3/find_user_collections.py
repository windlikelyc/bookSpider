# encoding:utf-8
# 查看用户收藏了多少本书
# 用户采用数据集中所有评论数目大于50本书的，调用API，用户有多个标签用逗号隔开

# num : 想要的用户数量
import json
import urllib2

import pymysql

insert_to_mysql = True
num_of_api = 0

def get_usesrs(num,offset=0):
    list_want = list()
    i = 1
    j = 1
    with open('users.dat', 'r') as f:
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
    return '("%s","%s","%s","%s","%s","%s","%s")'%(item['status'],item['rating'],item['updated'],item['comments'],item['tags'],item['book_id'],item['user_id'])

def get_html(uid,start,count):
    global num_of_api
    num_of_api = num_of_api + 1
    url = "https://api.douban.com/v2/book/user/%s/collections?apikey=0b2bdeda43b5688921839c8ecb20399b&start=%s&count=%s"%(uid,start,count)
    response = urllib2.urlopen(url)
    return json.loads(response.read())

# 返回uid的c条 有效 评论
def get_user_collections(uid,wanted_count,min_count = 5,max_count = 100,strict_comment=True,strict_rating=True,strict_tag = True):

    records = []
    un = open('user_unvalid.dat', 'a') # 记录没有评论的用户
    comments_count = 0
    html = get_html(uid,0,100) # 先试试水
    already = 0
    cycle = 0
    if html['total'] >= min_count :
        comments_count = html['total']
        num = min(100,html['total'])
        for i in range(num):
            try:
                tmp = dict()
                term = html['collections'][i]
                tmp['status'] = term['status']
                tmp['updated'] = term['updated']

                if strict_rating :
                    tmp['rating'] = term['rating']['value']
                else :
                    if term.get('rating','0') == '0':
                        tmp['rating'] = ''
                    else:
                        tmp['rating'] = term['rating']['value']
                if strict_comment :
                    tmp['comments'] = term['comments']
                else:
                    tmp['comments'] = term.get('comments','')

                if strict_tag:
                    tmp['tags'] = ','.join(term['tags'])
                else:
                    tmp['tags'] = term.get('tags', '')
                tmp['book_id'] = term['book_id']
                tmp['user_id'] = term['user_id']
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
                    term = html['collections'][i]
                    tmp['status'] = term['status']
                    tmp['updated'] = term['updated']

                    if strict_rating:
                        tmp['rating'] = term['rating']['value']
                    else:
                        if term.get('rating', '0') == '0':
                            tmp['rating'] = ''
                        else:
                            tmp['rating'] = term['rating']['value']
                    if strict_comment:
                        tmp['comments'] = term['comments']
                    else:
                        tmp['comments'] = term.get('comments', '')

                    if strict_tag:
                        tmp['tags'] = ','.join(term['tags'])
                    else:
                        tmp['tags'] = term.get('tags', '')
                    tmp['book_id'] = term['book_id']
                    tmp['user_id'] = term['user_id']
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
    list = get_usesrs(8000,offset=250)
    for i in range(len(list)):
        if insert_to_mysql:
            conn = pymysql.connect(host='39.106.39.216',
                                   user='root',
                                   passwd="admin123",
                                   db='doubandb_test',
                                   port=3306,
                                   charset='utf8')
            cursor = conn.cursor()

        per_user = get_user_collections(list[i],wanted_count=100,strict_comment=False,strict_rating=False)
        sql_list = []
        try:
            sql2 = 'Insert into user_collections_count (user_id,count) VALUES ("%s","%d")'%(list[i], per_user[1])
            print sql2
            if insert_to_mysql:
                cursor.execute(sql2)
                conn.commit()
        except Exception as e:
            pass
        for j in range(len(per_user[0])):
            try:
                sql = 'Insert into user_collections_1 (status,rating,updated,comments,tags,book_id,user_id) VALUES ' + get_para(per_user[0][j])
                print sql
                if insert_to_mysql:
                    cursor.execute(sql)
                    conn.commit()
            except Exception as e:
                pass






