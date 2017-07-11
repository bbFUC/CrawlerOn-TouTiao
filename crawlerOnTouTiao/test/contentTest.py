import urllib2
from bs4 import BeautifulSoup


if __name__ == '__main__':
    url = 'http://www.toutiao.com/a6398392407956685057/'
    print "123", url, 'rrrr'
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
            'Host': "www.toutiao.com",
            'Referer': "http://www.toutiao.com/",
            'X-Requested-With': "XMLHttpRequest",
            'Cookie': "csrftoken=4c9d92dba03a267de6bdb8d8d2a59802; tt_webid=56609842670; uuid='w:ccb829fa9020459cbe1024b623988c74'; _ga=GA1.2.188412771.1489068623; CNZZDATA1259612802=794809316-1489067802-%7C1489229849; UM_distinctid=15abc5cd6e92d2-0ff005b574fc54-1262694a-e1000-15abc5cd6ea151; utm_source=toutiao; __tasessionId=gkvfupjml1489230426764"
        }

    try:
        request = urllib2.Request(url, headers=headers)
        html = urllib2.urlopen(request, timeout=10).read()
        print html

    except Exception as e:
        print 'getHtmlError: ', e

    article_content = ['-1']
    try:
        soup = BeautifulSoup(html, 'html.parser')
        article_content = soup.select('.article-content')

    except Exception as e:
        print 'Beautiful Soup load error: ', e

    if article_content == ['-1']:
        print "error!"
    if article_content == []:
        print 'YES'
        article_content = soup.select('.answer-text-full')
        if article_content == []:
            print 'YES2'
            article_content = soup.select('.tt-ignored-node')
    news_list = []

    for news in article_content:
        content = news.get_text()
        news_list.append(content)
        print content
    print news_list
