# coding=utf-8

"""
在此处将获得的json文件保存到MongoDB
对于每个分类的新闻只有段子(joke)需要单独设立一个函数来建立符合自己结构的collection并存储,其他的新闻格式一样
新闻的具体内容article_content通过ArticleContentParser包里面的内容解析来获取
"""
import re
import time
from mylog import get_logger
from toutiaoparser.ArticleContentParser import ArticleContentParser
from MongoDBController import RecommendTypedNewsEngine
from MongoDBController import JokeNewsEngine
from OssStore import OssStore


class MongoDBStoreroom():
    def timeStampToDateTime(self, timeStamp):
        """
        将时间戳转换为年月日时间的形式
        """
        localTime = time.localtime(timeStamp)
        dateTime = time.strftime("%Y-%m-%d %H:%M:%S", localTime)
        return dateTime

    def dateTimeToTimeStamp(self, dateTime):
        """
        将年月日时间的形式转换为时间戳
        """
        timeArray = time.strptime(dateTime, "%Y-%m-%d %H:%M:%S")
        timeStamp = int(time.mktime(timeArray))
        return str(timeStamp)

    """
    这个模块待修改的地方是在collection储存的属性中加入'content'
    content获取的方式是打开新闻的url，然后用toutiaoparser中的模块来提取网页内容
    """
    def storeRecommendTypedNewsIntoMongoDB(self, jsonDict):
        """
        储存TouTiao_RECOMMEND等结构相似的实时新闻
        """
        jsonDataDict = jsonDict['data']
        articleContentParser = ArticleContentParser()  # 用来解析网页正文
        pattern = re.compile(r'http')  # 用来判断网页是否能被打开解析
        """
        将获取json文件的新闻装入collection
        """
        count = 1
        for newsObject in jsonDataDict:
            print u'Begin to get the ', count, u' news'
            # 提取第一个新闻的时间戳作为这个新闻包的时间戳
            if count == 1:
                newsTime = newsObject.get('behot_time')
            count = count + 1
            # 判断数据库是否已经存在这个新闻
            if (RecommendTypedNewsEngine.check_regular_obj(newsObject)):
                return True
                break

            try:
                # 判断获取的json文件正文能否被解析
                if newsObject.get('single_mode') is True:
                    temURL = newsObject.get('source_url')
                    """
                    此处的source_url不一定是头条自己的网址，可能是广告或者是其他新闻网站的地址
                    所以在任务执行过程中会出现html无法获取导致的getHTMLerror和Mongodb无法储存的错误
                    """
                    if pattern.match(temURL) is None:
                        targetURL = 'http://www.toutiao.com' + temURL
                        # 可被解析，则获取json文件里新闻的源网页url并进行解析
                        article_content = articleContentParser.getArticleContent(targetURL)
                    else:
                        article_content = []
                else:
                    article_content = []

                """
                此处没改为存储段子的形式,因为要提取新闻的内容,所以要给每个新闻对象创建一个'article_content'的属性,暂时还不清楚怎么添加所以依旧采用原来的形式。
                如果能够给对象添加'article_content'这个属性,那么只用修改MongoDBController.py中的类RecommendTypedNewsEngine的create_regular_obj(),
                在Create_regular_obj()函数中提取对象内容加上['group'][]即可
                """
                in_database = {
                    'chinese_tag': newsObject.get('chinese_tag'),
                    'media_avatar_url': newsObject.get('media_avatar_url'),
                    'tag_url': newsObject.get('news_entertainment'),
                    'title': newsObject.get('title'),
                    'abstract': newsObject.get('abstract'),
                    'gallary_image_count': newsObject.get('gallary_image_count'),
                    'image_list': newsObject.get('image_list'),
                    'behot_time': newsObject.get('behot_time'),
                    'source_url': newsObject.get('source_url'),
                    'source': newsObject.get('source'),
                    'more_mode': newsObject.get('more_mode'),
                    'single_mode': newsObject.get('single_mode'),
                    'middle_mode': newsObject.get('middle_mode'),
                    'article_genre': newsObject.get('article_genre'),
                    'comments_count': newsObject.get('comments_count'),
                    'has_gallery': newsObject.get('has_gallery'),
                    'tag': newsObject.get('tag'),
                    'image_url': newsObject.get('image_url'),
                    'group_id': newsObject.get('group_id'),
                    'article_content': article_content
                }
                # 将新闻保存在数据库中
                RecommendTypedNewsEngine.create_regular_obj(in_database)

                """
                然后这个部分把提取到的新闻image url的图片下载保存到oss云端
                """
                ossStore = OssStore()
                image_list = newsObject.get('image_list')
                newsType = newsObject.get('tag')
                newsTitle = newsObject.get('title')
                image_url = newsObject.get('image_url')
                if image_list:
                    imageCount = 0
                    for url in image_list:
                        imageUrl = url.get('url')
                        ossStore.save_image_in_oss(imageUrl, newsType, newsTime, newsTitle, imageCount)
                        imageCount = imageCount + 1
                else:
                    if image_url:
                        ossStore.save_image_in_oss(image_url, newsType, newsTime, newsTitle, 0)

            except Exception as e:
                print 'store Recommend-typed news into MongoDB error: ', e
                s = str(e)
                storeRecommendTypedNewsIntoMongoDBErrorMessage = get_logger('MongoDBStoreroom.log')
                storeRecommendTypedNewsIntoMongoDBErrorMessage.error('MongoDBStoreroom storeRecommendTypedNewsIntoMongoDB error: ' + s)

        return False

    def storeJokeIntoMongoDB(self, jsonDict):
        """
        储存TouTiao_JOKE实时新闻
        """
        jsonDataDict = jsonDict['data']

        """
        将获取json文件的新闻装入collection
        """
        count = 1
        for newsObject in jsonDataDict:
            print u'Begin to get the ', count, u' news'
            count = count + 1
            # 判断数据库是否已经存在这个新闻
            if JokeNewsEngine.check_joke_obj(newsObject):
                return True
                break

            try:
                JokeNewsEngine.create_joke_obj(newsObject)

            except Exception as e:
                print 'store JOKE into MongoDB error: ', e
                s = str(e)
                storeJokeIntoMongoDBErrorMessage = get_logger('MongoDBStoreroom.log')
                storeJokeIntoMongoDBErrorMessage.error('MongoDBStoreroom storeJokeIntoMongoDB error: ' + s)

        return False
