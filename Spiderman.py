# coding:utf-8
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
        self.manager.add_new_url(root_url)
        while(self.manager.has_new_url() ):
            # try:
                new_url = self.manager.get_new_url()
                html = self.downloader.download(new_url)
                new_urls,data = self.parser.parser(new_url,html)
                self.manager.add_new_urls(new_urls)
                self.output.store_into_database(data)
                print "已抓取%s个链接"%self.manager.old_url_size()
            # except Exception,e:
            #     print e

if __name__ == "__main__":
    spider = SpiderMan()
    book_id =
    spider.crawl("https://book.douban.com/subject/5363767/")