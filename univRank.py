import requests, bs4
from bs4 import BeautifulSoup
 
def getHTMLText(url):
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r.text
    except:
        return ""
 
def fillUnivList(ulist, html):
    soup = BeautifulSoup(html, "html.parser")
    for tr in soup.find('tbody').children:
        if isinstance(tr, bs4.element.Tag):
            tds = tr('td')
            ulist.append([tds[0].string, tds[1].string, tds[2].string, tds[3].string])
  
def main():
    uinfo = []
    url = 'http://www.zuihaodaxue.cn/zuihaodaxuepaiming2016.html'
    html = getHTMLText(url)
    fillUnivList(uinfo, html)
    with open('univ2016.csv', 'wt') as file:
        for item in uinfo:
            file.write('{},{},{},{}\n'.format(item[0], item[1], item[2], item[3]))


if __name__ == '__main__':
    main()
