#!/usr/bin/python2
# coding=utf-8
"""
程序主要内容：
从今日头条网站抓取带新闻的json包，解析后将其内容存入本地mongodb和阿里云。

程序结构解析：
CrawlerLoopControl用来控制爬虫的爬取类型:1.不断爬取最新内容 2.一直爬取到固定时间点(经测试大致能爬到4天之前的内容)
NewsParser来向目标url发送请求并拿回json文件
MongoDBController用来连接MongoDB,以及实现之后数据库存储的方法。这里面还有两个存recommendtypednews和jokenews的类
MongoDBStoreroom用来将获取的json文件提取关键信息并通过调用MongoDBController的两个类将信息存入mongodb。将图片存入oss也是在这里实现的
toutiaoparser装了不同模块urlopen(url).read()之后网页内容的提取器

程序尚存问题：
爬虫的cookie用的是我浏览器的cookie,在NewsParser中是写了自动获取cookie的函数的,但是我测试一直不成功,也就一直用的浏览器的cookie
没有固定时间超时处理机制,即程序会一直对一个新闻进行加载直至加载出来或者网站那边报错。所以程序开始进行下一个新闻的处理的时机就是直到这个新闻加载完或者过长时间没反应自动跳过
url_getter.timeStampURL中的网址还可以增多,只要是统一结构的新闻网址都可以直接添加网址使用
完善toutiaoparser包,这个包主要是打开网页解析网页中内容,现只有解析新闻具体内容的功能。新闻评论等都可以在这个包中添加
在MongoDBStoreroom中将图片存于阿里云仓库oss,oss存储目录结构在OssStore可以调整。另外没有对oss的保存和本地mongodb的保存进行并行,所以一个新闻储存完毕为存入mongodb的时间+存入oss的时间。若oss太长时间无法存储则程序会略过这个新闻进行下一个新闻的获取
"""

from CrawlerLoopControl import CrawlerLoopControl
from MongoDBController import MongoDBController
from config import mod_config
import url_getter.timeStampURL as TouTiaoNewsURL


def main():
    """
    输入想要查询的新闻时间戳和类型
    时间戳形式:2017-03-17 20:05:32
    新闻类型:'recommend','hot','image','joke','society','entertainment','tech','sports','car','finance','funny'
    """
    hot_timeStamp = mod_config.get_config('crawler', 'timeStamp')  # 输入想要查询的新闻时间戳 '0'表示最新新闻，'2017-03-15 18:23:05'表示从当前时间的新闻一直记录到目标时间点
    newsType = mod_config.get_config('crawler', 'newsType')  # 输入想要查询的新闻类型
    url = TouTiaoNewsURL.getTargetURL(newsType, '0')  # 获得目标url
    print 'url get: ', url
    """
    获取MongoDB用户端口，连接mongodb
    """
    mongoDataBase = mod_config.get_config('mongodb', 'database_name')
    mongoHost = mod_config.get_config('mongodb', 'host')
    mongoPort = mod_config.get_config('mongodb', 'port')

    """
    连接数据库
    """
    MongoDBController(mongoDataBase, mongoHost, int(mongoPort)).connectToMongoDB()
    """
    此处可以调用爬虫api来控制爬取新闻的类型
    """
    crawler = CrawlerLoopControl()
    print 'crawler control constructed'
    if mod_config.get_config('crawler', 'crawlerMode') == 'timestamp':
        crawler.getTimeStampNewsLooply(hot_timeStamp, newsType, url)
    elif mod_config.get_config('crawler', 'crawlerMode') == 'newest':
        crawler.getRecentNewsLooply(newsType, url)


if __name__ == '__main__':
    main()
