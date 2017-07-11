# coding=utf-8
"""
用来控制爬虫搜集新闻的类型(循环搜索最新闻，按时间点搜索)

循环爬取的原理是第一次向目标url发送请求拿回来一个json包,json包存了一个next_behot_time就是下一个时间点的json包,
然后请求具有此时间点的json包然后就可以一直顺着获得越来越早的新闻
"""

from toutiaoparser.NewsParser import NewsParser
from MongoDBStoreroom import MongoDBStoreroom
import url_getter.timeStampURL as TouTiaoNewsURL
from mylog import get_logger

class CrawlerLoopControl():
    def __init__(self):
        """
        建立控制mongodb存储json文件的对象
        """
        self.mongoDBStoreroom = MongoDBStoreroom()

    """
    下一步在函数里加入根据newsType不同调用不同存储方式的判断
    """
    def getTimeStampNewsLooply(self, hot_timeStamp, newsType, url):
        """
        根据时间戳判断是否一直获取到目标时间点新闻
        """
        print '-----------------------Begin to crawl------------------------'
        print '----------------Crawler Mode: TimeStampCrawler---------------'
        print '------------------Target timestamp confirmed-----------------'
        print '---------------------' + hot_timeStamp + '--------------------'
        print '------------------Target news type confirmed-----------------'
        print '-----------------News Type: ' + newsType + '---------------------'
        crawlerLoopControlMessage = get_logger('CrawlerControl.log')
        crawlerLoopControlMessage.info('Begin to crawl')
        crawlerLoopControlMessage.info('Crawler Mode: TimeStampCrawler')
        crawlerLoopControlMessage.info('Target timestamp: ' + hot_timeStamp)
        crawlerLoopControlMessage.info('News type: ' + newsType)

        count = 1
        nextNewsType = newsType  # 继续爬取的新闻类型  
        targetTimeStamp = TouTiaoNewsURL.dateTimeToTimeStamp(hot_timeStamp)  # 将目标日期转换为时间戳str
        intTargetTimeStamp = int(targetTimeStamp)  # str--->int
        jsonDictPage = NewsParser().getJsonByRequests(url)  # 获取json文件
        nextJsonPage = jsonDictPage['next']['max_behot_time']  # 获取下一个json文件时间戳
        print 'target time stamp is: ', intTargetTimeStamp
        # 一直抓取json文件直到到达目标时间戳
        while intTargetTimeStamp < nextJsonPage:
            print u'Entering the', count, u' round crawl'
            if newsType == 'joke':
                flag = self.mongoDBStoreroom.storeJokeIntoMongoDB(jsonDictPage)
            else:
                flag = self.mongoDBStoreroom.storeRecommendTypedNewsIntoMongoDB(jsonDictPage)

            # 增量更新标志,如果flag=true说明在这之前的新闻已经爬取过任务可以终止了
            if flag:
                break

            nextUrl = TouTiaoNewsURL.getTargetURL(nextNewsType, str(nextJsonPage))
            jsonDictPage = NewsParser().getJsonByRequests(nextUrl)
            nextJsonPage = jsonDictPage['next']['max_behot_time']
            print 'json file time stamp is: ', nextJsonPage
            print count, ' Json files have been stored'
            print u'the ', count, u' round ended'
            count = count + 1

        print '-------------------target time stamp has reached-------------------'
        print '------------------------crawl mission done-------------------------'

    def getRecentNewsLooply(self, newsType, url):
        print '-----------------------Begin to crawl------------------------'
        print '--------------Crawler Mode: RecentNewsCrawler----------------'
        print '------------------Target news type confirmed-----------------'
        print '-----------------News Type: ' + newsType + '---------------------'
        crawlerLoopControlMessage = get_logger('CrawlerControl.log')
        crawlerLoopControlMessage.info('Begin to crawl')
        crawlerLoopControlMessage.info('Crawler Mode: RecentNewsCrawler')
        crawlerLoopControlMessage.info('News type: ' + newsType)

        count = 1
        jsonDictPage = NewsParser().getJsonByRequests(url)
        # 默认一直抓取新闻
        while True:
            print u'Entering the ', count, u' round crawl'
            if newsType == 'joke':
                self.mongoDBStoreroom.storeJokeIntoMongoDB(jsonDictPage)
            else:
                self.mongoDBStoreroom.storeRecommendTypedNewsIntoMongoDB(jsonDictPage)

            nextUrl = url
            jsonDictPage = NewsParser().getJsonByRequests(nextUrl)
            print count, ' Json files have been stored'
            print u'the ', count, u' round ended'
            count = count + 1

        print '-----------------------crawl mission done--------------------------'
