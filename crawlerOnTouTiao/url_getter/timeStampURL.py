# coding=utf-8
"""
用来对url的时间戳进行修改
"""

import time

"""
保存今日头条各个页面获取json文件请求的url
其中max_behot_time=0意味着请求当前最新消息
头条新闻图片默认请求的是当前时间的时间戳，但是改为0不影响请求
有的板块新闻的属性是一致的，有的板块差别很大，因此需要建立在mongodb建立几种不同的collection来储存新闻
由于这些请求都是当前的，所以如果需要获取特定时间的新闻需要修改max_behot_time

经测试，输入过去时间节点的时间戳不能直接获取当时时间的新闻，但是从后往前的做法不行，从前往后可以:在主页不断下拉的过程中，收获的json包会有一个next属性记录着下一个将要获得的json包的时间戳，按照这个时间戳不断获取新闻即可
"""


def timeStampToDateTime(timeStamp):
    """
    将时间戳转换为年月日时间的形式
    """
    localTime = time.localtime(timeStamp)
    dateTime = time.strftime("%Y-%m-%d %H:%M:%S", localTime)
    return dateTime


def dateTimeToTimeStamp(dateTime):
    """
    将年月日时间的形式转换为时间戳
    """
    timeArray = time.strptime(dateTime, "%Y-%m-%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray))
    return str(timeStamp)


def getTargetURL(urlType, behot_time):
    if (urlType == 'recommend'):
        TOUTIAO_RECOMMEND = 'http://www.toutiao.com/api/pc/feed/?category=__all__&utm_source=toutiao&widen=1&max_behot_time=' + behot_time + '&max_behot_time_tmp=' + behot_time + '&tadrequire=true&as=A185486CC7A6246&cp=58C766D2F4961E1'
        return TOUTIAO_RECOMMEND
    elif (urlType == 'hot'):
        TOUTIAO_HOT = 'http://www.toutiao.com/api/pc/feed/?category=news_hot&utm_source=toutiao&widen=1&max_behot_time=' + behot_time + '&max_behot_time_tmp=' + behot_time + '&tadrequire=true&as=A1B5882CF717265&cp=58C787C2E6759E1'
        return TOUTIAO_HOT
    elif (urlType == 'image'):
        TOUTIAO_IMAGE = 'http://www.toutiao.com/api/article/recent/?source=2&count=20&category=gallery_detail&max_behot_time=' + behot_time + '&utm_source=toutiao&device_platform=web&offset=0&as=A1A5C8DC47E7379&cp=58C7D7D347092E1&_=1489466233230'
        return TOUTIAO_IMAGE
    elif (urlType == 'joke'):
        TOUTIAO_JOKE = 'http://www.toutiao.com/api/article/feed/?category=essay_joke&utm_source=toutiao&widen=1&max_behot_time=' + behot_time + '&max_behot_time_tmp='+ behot_time + '&tadrequire=true&as=A185685C2991CB3&cp=58C9719C0B937E1'
        return TOUTIAO_JOKE
    elif (urlType == 'society'):
        TOUTIAO_SOCIETY = 'http://www.toutiao.com/api/pc/feed/?category=news_society&utm_source=toutiao&widen=1&max_behot_time=' + behot_time + '&max_behot_time_tmp=' + behot_time + '&tadrequire=true&as=A125E82C39F5A0D&cp=58C9D5BAC00D4E1'
        return TOUTIAO_SOCIETY
    elif (urlType == 'entertainment'):
        TOUTIAO_ENTERTAINMENT = 'http://www.toutiao.com/api/pc/feed/?category=news_entertainment&utm_source=toutiao&widen=1&max_behot_time=' + behot_time + '&max_behot_time_tmp=' + behot_time + '&tadrequire=true&as=A105486C6925A85&cp=58C9C58A48554E1'
        return TOUTIAO_ENTERTAINMENT
    elif (urlType == 'tech'):
        TOUTIAO_TECH = 'http://www.toutiao.com/api/pc/feed/?category=news_tech&utm_source=toutiao&widen=1&max_behot_time=' + behot_time + '&max_behot_time_tmp=' + behot_time + '&tadrequire=true&as=A1D5182CF955B9D&cp=58C9E5DB795D8E1'
        return TOUTIAO_TECH
    elif (urlType == 'sports'):
        TOUTIAO_SPORTS = 'http://www.toutiao.com/api/pc/feed/?category=news_sports&utm_source=toutiao&widen=1&max_behot_time=' + behot_time + '&max_behot_time_tmp=' + behot_time + '&tadrequire=true&as=A185687CC905BF8&cp=58C9F52B2F283E1'
        return TOUTIAO_SPORTS
    elif (urlType == 'car'):
        TOUTIAO_CAR = 'http://www.toutiao.com/api/pc/feed/?category=news_car&utm_source=toutiao&widen=1&max_behot_time=' + behot_time + '&max_behot_time_tmp=' + behot_time + '&tadrequire=true&as=A1C548EC29E5C60&cp=58C9E58C36E0BE1'
        return TOUTIAO_CAR
    elif (urlType == 'finance'):
        TOUTIAO_FINANCE = 'http://www.toutiao.com/api/pc/feed/?category=news_finance&utm_source=toutiao&widen=1&max_behot_time=' + behot_time + '&max_behot_time_tmp=' + behot_time + '&tadrequire=true&as=A185887CE9E5CD1&cp=58C9650C0DB15E1'
        return TOUTIAO_FINANCE
    elif (urlType == 'funny'):
        TOUTIAO_FUNNY = 'http://www.toutiao.com/api/pc/feed/?category=funny&utm_source=toutiao&widen=1&max_behot_time=' + behot_time + '&max_behot_time_tmp=' + behot_time + '&tadrequire=true&as=A10588FC59D5D27&cp=58C9D59D02979E1'
        return TOUTIAO_FUNNY
    else:
        print 'wrong news category!'
