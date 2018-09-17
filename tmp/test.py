import bs4
from bs4 import BeautifulSoup
import requests


if __name__=='__main__':

    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5 ; Windows NT)'
    headers = {'User-Agent':user_agent}
    r = requests.get('http://seputu.com/',headers = headers)
    soup = BeautifulSoup(r.text,'html.parser',from_encoding='utf-8')
    for mulu in soup.find_all(class_="mulu"):
        h2 = mulu.find('h2')
        if h2 != None:
            h2_title = h2.string
            for a in mulu.find(class_='box').find_all('a'):
                href = a.get('href')
                box_title = a.get('title')
                print href,box_title





