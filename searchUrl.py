import requests, re
from urllib.request import quote
from bs4 import BeautifulSoup

headers = {
'Host': 'www.baidu.com',
'Connection': 'keep-alive',
'Cache-Control': 'max-age=0',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
'Accept-Encoding': 'gzip, deflate, sdch',
'Accept-Language': 'zh-CN,zh;q=0.8'
}

def get_res(url):
    try:
        res = requests.get(url, headers = headers, timeout = 1.5)
        res.raise_for_status()
        #res.encoding = 'utf-8'
        return res
    except Exception as ex:
        print('[-]ERROR: ' + str(ex))
        return res              #有时会有404 Client Error: Not Found for url，其实url是有的

def complete_url(href):         #有些长地址会有缺省，需另外请求
    try:
        print('[+]查询完整URL ...')
        url = get_res(href).url
        return url
    except:
        return ''

def parse_res(res_text):
    try:
        soup = BeautifulSoup(res_text, 'html.parser')
        content = soup.select('#content_left > div.result')
        return content
    except Exception as ex:
        print('[-]ERROR: parse error-{}\n'.format(ex.message))

def match_url(content):
    url = ''
    for item in content:        #先找官网标志
        h3 = item.select('h3 > a')
        f13 = item.select('.f13 > a')
        if len(h3) == 2:
            text = h3[1].get_text()
            if text == '官网' and f13 != []:
                url = f13[0].get_text()
                url = re.sub(r'\xa0', '', url)
                if re.search(r'\.{2,}', url):
                    href = f13[0].attrs['href']
                    url = complete_url(href)
                break
    for item in content:        #无官网标志返回第一个
        if url:
            break
        f13 = item.select('.f13 > a')
        if f13 != []:
            url = f13[0].get_text()
            url = re.sub(r'\xa0', '', url)
            if re.search(r'\.{2,}', url):
                href = f13[0].attrs['href']
                url = complete_url(href)
            break
    url = re.sub('http://|index.php|index.html|default.html', '', url)
    return url

def search(keyword):
    search_url = 'https://www.baidu.com/s?wd={}&ie=UTF-8'.format(quote(keyword))
    try:
        res = get_res(search_url)
        html = res.text
        content = parse_res(html)
        url = match_url(content)
        return url
    except:
        return None
