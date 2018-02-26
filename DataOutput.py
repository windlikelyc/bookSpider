# encoding:utf-8
import codecs
import pymysql
class DataOutput(object):
    def __init__(self):
        self.datas=[]
        self.conn = pymysql.connect(host='39.106.39.216',
                               user='root',
                               passwd="admin123",
                               db='doubandb',
                               port=3306,
                               charset='utf8')
        self.cursor = self.conn.cursor()

    def store_data(self,data):
        if data is None:
            return
        self.datas.append(data)

    def output_html(self):
        fout = codecs.open('baike.html','w',encoding='utf-8')
        fout.write("<html>")
        fout.write("<body>")
        fout.write("<table>")
        for data in self.datas:
            fout.write("<tr>")
            fout.write("<td>%s<td>"%data['url'])
            fout.write("<td>%s<td>"%data['title'])
            fout.write("<td>%s<td>"%data['summary'])
            fout.write("</tr>")
        fout.write("<html>")
        fout.write("<body>")
        fout.write("<table>")
        fout.close()

    def store_into_database(self,alldata):
        try:
            book_id = alldata['book_id']
            datas = alldata['list']
            for data in datas:
                book_data = "'%s','%s','%s','%s','%s','%s' " % (data['user_id'], data['user_name'].replace("'", "\\\'"), data['rating'], data['comment'], book_id , data['time'])
                user_sql = 'INSERT INTO user_book_rating (userid,user_name,rating,comment,bookid,time) VALUES(' + book_data + ');'
                self.cursor.execute(user_sql)
                self.conn.commit()
        except Exception as e:
            print e
