# coding=utf-8

import urllib2
import cookielib
import json


def main():
    """
    cookie = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    response = opener.open('https://www.baidu.com')
    print cookie
    """
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
        'Host':
        "www.toutiao.com",
        'Referer':
        "http://www.toutiao.com/",
        'X-Requested-With':
        "XMLHttpRequest",
        'Cookie':
        'csrftoken=4c9d92dba03a267de6bdb8d8d2a59802; tt_webid=56609842670; uuid="w:ccb829fa9020459cbe1024b623988c74"; _ga=GA1.2.188412771.1489068623; CNZZDATA1259612802=794809316-1489067802-%7C1489229849; UM_distinctid=15abc5cd6e92d2-0ff005b574fc54-1262694a-e1000-15abc5cd6ea151; utm_source=toutiao; __tasessionId=gkvfupjml1489230426764'
    }
    url = 'http://www.toutiao.com/api/pc/feed/?category=__all__&utm_source=toutiao&widen=1&max_behot_time=0&max_behot_time_tmp=0&tadrequire=true&as=A19569D0E4FBB4D&cp=5904DB4BB4ADFE1'# 'http://www.toutiao.com/api/article/feed/?category=essay_joke&utm_source=toutiao&widen=1&max_behot_time=1489761311&max_behot_time_tmp=1489761311&tadrequire=true&as=A1E5E80C1B8F5E5&cp=58CB5F750E05BE1'
    try:
        request = urllib2.Request(url, headers=headers)
        print "+"*60
        jsonDict = json.loads(urllib2.urlopen(request).read())
        print 60*'-'

        jsonDataDict = jsonDict['data']
        for news in jsonDataDict:
            # print type(news)
            # print type(news['group'])
            # groupObject1 = news['group']['text']
            # print groupObject1
            # print type(groupObject1)
            imageList = news.get('image_list')
            print type(imageList)
            print u'草泥马'
            if imageList:
                for url in imageList:
                    print type(url)
                    print url
                    print type(url.get('url'))
                    print url.get('url')

        # print jsonDataDict
        print "+"*60

    except Exception as e:
        print 'jsonParserError: ', e


if __name__ == '__main__':
    main()