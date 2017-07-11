# coding=utf-8
"""
ArticleContentParser打开网页将网页里面的文字内容全部保存下来

还有一个类用来获取评论的json文件把评论也扒下来
"""

from mylog import get_logger
from NewsParser import NewsParser
from bs4 import BeautifulSoup


class ArticleContentParser():
    def __init__(self):
        self.htmlGetter = NewsParser()

    def getArticleContent(self, url):
        article_content = ['-1']  # 初始化,如果html无法打开,beautifulsoup无法读取则可直接返回空值
        news_list = []  # 用来存放新闻

        try:
            html = self.htmlGetter.getHtmlByRequests(url)
            soup = BeautifulSoup(html, 'html.parser')
            article_content = soup.select('.article-content')

        except Exception as e:
            print 'Beautiful Soup load error: ', e
            s = str(e)
            getArticleContentError = get_logger('ArticleContentParser.log')
            getArticleContentError.error = ('ArticleContentParser getArticleContentError Beautiful soup load error: ' + s)

        # 如果前面出现错误直接返回空值
        if article_content == ['-1']:
            return news_list
        # 判断是不是另一种问答形式文本
        if article_content == []:
            article_content = soup.select('.answer-text-full')
            """
            由于这种类型的网页不更改header无法直接通过toutiao+/group/id的形式打开，所以解析网页也没有什么意义
            if article_content == []:
                article_content = soup.select('.tt-ignored-node')
            """

        for news in article_content:
            newsText = news.get_text()
            news_list.append(newsText)

        return news_list
