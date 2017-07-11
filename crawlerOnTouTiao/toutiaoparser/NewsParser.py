# coding=utf-8

"""
NewsParser用来向今日头条网页发送请求并拿回json文件

getCookie(self,url):访问一次今日头条主页获得cookie


"""

import urllib2
import cookielib
import json
from mylog import get_logger


class NewsParser():
    def __init__(self):
        self.baseURL = "https://www.toutiao.com"

    """
    这样得到的cookie一个是有格式问题，另一个感觉今日头条返回的cookie不是像浏览器上能用的cookie
    """
    def getCookie(self):
        cookie = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
        opener.open(self.baseURL)
        return cookie

    def getHtmlByRequests(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
            'Host': "www.toutiao.com",
            'Referer': "http://www.toutiao.com/",
            'X-Requested-With': "XMLHttpRequest",
            'Cookie': "csrftoken=4c9d92dba03a267de6bdb8d8d2a59802; tt_webid=56609842670; uuid='w:ccb829fa9020459cbe1024b623988c74'; _ga=GA1.2.188412771.1489068623; CNZZDATA1259612802=794809316-1489067802-%7C1489229849; UM_distinctid=15abc5cd6e92d2-0ff005b574fc54-1262694a-e1000-15abc5cd6ea151; utm_source=toutiao; __tasessionId=gkvfupjml1489230426764"
        }

        try:
            request = urllib2.Request(url, headers=headers)
            htmlPage = urllib2.urlopen(request).read()

        except Exception as e:
            print 'getHtmlError: ', e
            print 'The URL: ', url, " can't open"  # 这个无法打开的url可以记录在log中
            s = str(e)
            getHtmlByRequestsError = get_logger('NewsParserError.log')
            getHtmlByRequestsError.error('getHtmlByRequestsError getHtmlError: ' + s + '\nThe unopened URL: ' + url)

        return htmlPage

    def getJsonByRequests(self, url):
        # cookie = self.getCookie()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
            'Host': "www.toutiao.com",
            'Referer': "http://www.toutiao.com/",
            'X-Requested-With': "XMLHttpRequest",
            'Cookie': "csrftoken=4c9d92dba03a267de6bdb8d8d2a59802; tt_webid=56609842670; uuid='w:ccb829fa9020459cbe1024b623988c74'; _ga=GA1.2.188412771.1489068623; CNZZDATA1259612802=794809316-1489067802-%7C1489229849; UM_distinctid=15abc5cd6e92d2-0ff005b574fc54-1262694a-e1000-15abc5cd6ea151; utm_source=toutiao; __tasessionId=gkvfupjml1489230426764"
        }

        try:
            request = urllib2.Request(url, headers=headers)
            page = urllib2.urlopen(request).read()
            data = json.loads(page)

        except Exception as e:
            print 'getJsonError: ', e
            s = str(e)
            getJsonByRequestsError = get_logger('NewsParserError.log')
            getJsonByRequestsError.error('getJsonByRequestsError getJsonError: ' + s)

        return data
