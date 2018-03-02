# coding:utf-8
import requests
import time
import json
class HtmlDownloader(object):

    def __init__(self):
        self.index = 0
        self.proxies = self.get_proxy()

    # 返回有效的ip的地址
    def get_proxy(self):

        r = requests.get('http://127.0.0.1:8000/?types=2')
        ip_ports = json.loads(r.text)
        self.index = self.index + 1

        ip = ip_ports[self.index][0]
        port = ip_ports[self.index][1]

        headers = {'User-Agent': 'Mozilla/4.0 (compatible;MSIE 5.5;Windows NT', 'Connection': 'close'}
        proxies = {
            'http': 'http://%s:%s' % (ip, port),
            'https': 'http://%s:%s' % (ip, port)
        }

        while self.index < 100:
            try:
                #没必要用豆瓣试试水
                r = requests.get('http://www.baidu.com', headers=headers, proxies=proxies, timeout=5)
                return proxies
            except Exception as e:
                time.sleep(5)
                self.index= self.index + 1
                ip = ip_ports[self.index][0]
                port = ip_ports[self.index][1]
                proxies = {
                    'http': 'http://%s:%s' % (ip, port),
                    'https': 'http://%s:%s' % (ip, port)
                }

        print "已达到100次代理尝试"

    def download(self,url):
        if url is None:
            return None

        headers = {'User-Agent': 'Mozilla/4.0 (compatible;MSIE 5.5;Windows NT','Connection': 'close'}

        #如果去掉这句话就变成了不使用代理
        while True:
            try:
                r = requests.get(url,headers=headers,proxies=self.proxies,timeout=5)
                if r.status_code == 200:
                    r.encoding = 'utf-8'
                    if r.text.encode('unicode-escape').decode('string_escape').find("Unauthorized") != -1:
                        raise RuntimeError(r.text.encode('unicode-escape').decode('string_escape'))
                    return r.text
                else:
                    raise RuntimeError('得不到正确得代理，从新找代理')

            except Exception as e:
                self.proxies = self.get_proxy()
                time.sleep(5)


        return None

