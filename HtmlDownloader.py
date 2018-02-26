# coding:utf-8
import requests
import time
import json
class HtmlDownloader(object):

    def __init__(self):
        self.pro = {}



    # 返回有效的ip的地址
    def get_proxy(self):

        r = requests.get('http://127.0.0.1:8000/?types=0&count=100&country=国内')
        ip_ports = json.loads(r.text)
        index = 0

        ip = ip_ports[0][0]
        port = ip_ports[0][1]

        headers = {'User-Agent': 'Mozilla/4.0 (compatible;MSIE 5.5;Windows NT'}
        proxies = {
            'http': 'http://%s:%s' % (ip, port),
            'https': 'http://%s:%s' % (ip, port)
        }

        while index < 100:
            try:
                r = requests.get('www.douban.com', headers=headers, proxies=proxies, timeout=5)
                return proxies
            except Exception as e:
                index= index + 1


    def download(self,url):
        if url is None:
            return None

        headers = {'User-Agent': 'Mozilla/4.0 (compatible;MSIE 5.5;Windows NT'}

        while True:
            try:
                r = requests.get(url,headers=headers,proxies=self.proxies,timeout=5)
                break
            except Exception as e:
                self.proxies = self.get_proxy()

        if r.status_code == 200:
            r.encoding = 'utf-8'
            return r.text

        return None

