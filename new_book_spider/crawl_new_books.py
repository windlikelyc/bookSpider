#
import re

import pymysql
import requests
import time
from bs4 import BeautifulSoup

r = requests.get('https://book.douban.com/latest?icn=index-latestbook-all').text
soup = BeautifulSoup(r, 'html.parser', from_encoding='utf-8')
conn = pymysql.connect(host='39.106.39.216',
                            user='root',
                            passwd="admin123",
                            db='doubandb',
                            port=3306,
                            charset='utf8')
cursor = conn.cursor()
comments = soup.find(class_='cover-col-4 clearfix').find_all('li')
for child in comments:
    try:
        img = child.find_all('a')[0].img['src']
        href = child.find_all('a')[0]['href']
        title = unicode(child.find_all('a')[1].string)
        rate = unicode(child.find(class_='font-small color-lightgray').string).strip()
        author_and_date = unicode(child.find(class_='color-gray').string).strip()
        pubdate = author_and_date.split('/')[-1]
        detail = unicode(child.find(class_='detail').string).strip()
        id = child.find_all('a')[0]['href'].split('/')[-2]
        book_data = "'%s','%s','%s','%s','%s','%s','%s','%s' "%(id,title,author_and_date,pubdate,img,rate,href,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        user_sql = 'INSERT INTO book_new (id,title,publisher_and_author,pubdate,img,rate,href,create_time) VALUES(' + book_data + ');'
        cursor.execute(user_sql)
        conn.commit()
    except Exception as e:
        print e
conn.close()
