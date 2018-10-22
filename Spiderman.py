# coding:utf-8
import time

from DataOutput import DataOutput
from HtmlDownloader import HtmlDownloader
from HtmlParser import HtmlParser
from UrlManager import UrlManager
class SpiderMan(object):
    def __init__(self):
        self.manager = UrlManager()
        self.downloader = HtmlDownloader()
        self.parser = HtmlParser()
        self.output = DataOutput()

    def crawl(self,root_url):
        listWant = list()
        listAlr = list()
        with open('wanted', 'r') as f:
            for line in f.readlines():
                listWant.append(line.strip())
        with open('already', 'r') as f:
            for line in f.readlines():
                listAlr.append(line.strip())
        bookIdList = list(set(listWant).difference(set(listAlr)))
        count = len(bookIdList) - 1
        url_1 = "https://book.douban.com/subject/"
        url_2 = "/comments"
        f = open('already', 'a')
        log = open('log', 'a')
        while count > 0 :
            try:
                new_url = url_1 + bookIdList[count] + url_2
                html = self.downloader.download(new_url)
                new_urls, data = self.parser.parser(new_url, html)
                self.manager.add_new_urls(new_urls)
                self.output.store_into_database(data)
                while(self.manager.new_url_size() > 0):
                    new_url = self.manager.get_new_url()
                    html = self.downloader.download(new_url)
                    new_urls,data = self.parser.parser(new_url,html) # 这里不加入new url
                    self.output.store_into_database(data)
                f.write(bookIdList[count])
                f.write('\n')
                f.flush()
            except Exception as e:
                now = int(round(time.time() * 1000))
                now02 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(now / 1000))
                log.write(now02 + str(e) + ' ')
                log.write(bookIdList[count] + '写入失败')
                log.write('\n')
                log.flush()
                log.write(str(e))
            finally:
                time.sleep(5)
                count = count - 1

if __name__ == "__main__":
    spider = SpiderMan()
    spider.crawl("https://book.douban.com/subject/5363767/")