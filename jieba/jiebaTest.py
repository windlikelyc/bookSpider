# encoding=utf-8
import jieba
import pymysql

#  这是一个简单的结巴分词api测试脚本。
if __name__=='__main__':
        datas = []
        db = pymysql.connect(host='39.106.39.216',user='root',passwd="admin123",db='doubandb',port=3306,charset='utf8',cursorclass=pymysql.cursors.SSDictCursor)
        # -------------在这里写你需要执行的语句------------
        sql = 'SELECT * FROM `book_summery` WHERE book_summery != "" LIMIT 20; '
        with db.cursor() as src_cursor:
            src_cursor.execute(sql)
            result = src_cursor.fetchone()

            while result is not None:
                result = result['book_summery']



                seg_list = jieba.cut("上海自来水来自海上", cut_all=False)
                for a in seg_list:
                    print a
                print "-------------------------------"










                result = src_cursor.fetchone()
        db.close()


