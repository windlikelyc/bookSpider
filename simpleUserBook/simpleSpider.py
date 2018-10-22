# encoding=utf-8

import io
import requests
import time
import json
import time
# 爬虫主程序

headers = {
    'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
    'Accept-Language': 'zh-Hans-CN, zh-Hans; q=0.5',
    'Connection': 'Keep-Alive',
    'Cookie': 'bid=lkpO8Id/Kbs; __utma=30149280.1824146216.1438612767.1440248573.1440319237.13; __utmz=30149280.1438612767.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); as=http://book.douban.com/people/133476248/; ll=108288; viewed=26274009_1051580; ap=1; ps=y; ct=y; __utmb=30149280.23.10.1440319237; __utmc=30149280; __utmt_douban=1; _pk_id.100001.3ac3=b288f385b4d73e38.1438657126.3.1440319394.1440248628.; __utma=81379588.142106303.1438657126.1440248573.1440319240.3; __utmz=81379588.1440319240.3.2.utmcsr=movie.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; _pk_ses.100001.3ac3=*; __utmb=81379588.23.10.1440319240; __utmt=1; __utmc=81379588; _pk_ref.100001.3ac3=%5B%22%22%2C%22%22%2C1440319240%2C%22http%3A%2F%2Fmovie.douban.com%2F%22%5D',
    'Host': 'book.douban.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240'}

initsleeptime = 10

def crawl(url):
    pass

# 记录主程序
def run():
    listWant = list()
    listAlr = list()
    with open('wanted', 'r') as f:
        for line in f.readlines():
            listWant.append(line.strip())
    with open('already','r') as f:
        for line in f.readlines():
            listAlr.append(line.strip())
    bookIdList = list(set(listWant).difference(set(listAlr)))
    count = len(bookIdList) - 1
    url_1 = "https://book.douban.com/subject/"
    url_2 = "/comments/hot"
    f = open('already','a')
    log = open('log','a')
    sleeptime = initsleeptime
    while count != -1:
        try:
            url = url_1 + bookIdList[count] + url_2
            r = requests.get(url, headers=headers, timeout=5)
            if r.status_code == 200:
                r.encoding = 'utf-8'
                if r.text.encode('unicode-escape').decode('string_escape').find("Unauthorized") != -1:
                    raise RuntimeError(r.text.encode('unicode-escape').decode('string_escape'))
                sleeptime = initsleeptime # 恢复初始沉睡时间
            else:
                raise RuntimeError('得不到正确得代理，从新找代理')
            f.write(bookIdList[count])
            f.write('\n')
            f.flush()
            count = count - 1
        except Exception as e:
            now = int(round(time.time() * 1000))
            now02 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(now / 1000))
            log.write(now02 + str(e)+' ')
            log.write(bookIdList[count]+'写入失败')
            log.write('当前sleep时间为：' + sleeptime)
            log.write('\n')
            log.flush()
            count = count -1
            sleeptime = sleeptime * 2
        finally:
            time.sleep(sleeptime)
    f.close()
    log.close()
if __name__ == "__main__":
    run()





