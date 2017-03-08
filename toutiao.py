# -*- coding: UTF-8 -*-
import time
import re
import csv

from selenium import webdriver
from bs4 import BeautifulSoup

import constant.toutiao as toutiao


"""
def get_page(url):
    print u"开始request"
    print url
    request = urllib2.Request(url)
    print request
    request.add_header(
        "User-Agent",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:46.0) Gecko/20100101 Firefox/46.0"
    )
    page = urllib2.urlopen(request)
    print u"网页源码已获得"
    print page
    return page
"""

def get_page(url):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(1)
    driver.execute_script("window.scrollBy(0, 10000)", "")
    time.sleep(4)
    page = driver.page_source
    driver.close()
    return page

def get_news(csv_file, url, category):
    writer = csv.writer(csv_file)

    link_head = 'https://toutiao.com'
    soup = BeautifulSoup(get_page(url), "html.parser")
    items = soup.find_all("div", {"class": "item-inner"})
    
    #新闻个数
    print u"items的数量是:", len(items)
    #获取新闻题目链接和图片链接
    for i in range(0, len(items)):
        if len(items[i].select('img')) == 0:
            print '0'
            title = items[i].select('div[class="title-box"]')[0].get_text().strip().encode('GBK', 'ignore')
            link = link_head + items[i].select('div[class="title-box"]')[0].a['href'].strip()
            writer.writerow(("", "", "", title, link, 0, category))

        elif len(items[i].select('img')) == 1:
            print '1'
            image = items[i].select('img')[0].get('src')
            title = items[i].select('div[class="title-box"]')[0].get_text().strip().encode('GBK', 'ignore')
            link = link_head + items[i].select('div[class="title-box"]')[0].a['href'].strip()
            writer.writerow((image, "", "", title, link, 1, category))

        elif len(items[i].select('img')) == 2:
            print '2'
            image1 = items[i].select('img')[0].get('src')
            image2 = items[i].select('img')[1].get('src')
            title = items[i].select('div[class="title-box"]')[0].get_text().strip().encode('GBK', 'ignore')
            link = link_head + items[i].select('div[class="title-box"]')[0].a['href'].strip()
            writer.writerow((image1, image2, "", title, link, 2, category))

        elif len(items[i].select('img')) == 3:
            print '3'
            image1 = items[i].select('img')[0].get('src')
            image2 = items[i].select('img')[1].get('src')
            image3 = items[i].select('img')[2].get('src')
            title = items[i].select('div[class="title-box"]')[0].get_text().strip().encode('GBK', 'ignore')
            link = link_head + items[i].select('div[class="title-box"]')[0].a['href'].strip()
            writer.writerow((image1, image2, image3, title, link, 3, category))

        else:
            print '4'
            image1 = items[i].select('img')[0].get('src')
            image2 = items[i].select('img')[1].get('src')
            image3 = items[i].select('img')[2].get('src')
            image4 = items[i].select('img')[3].get('src')
            title = items[i].select('div[class="title-box"]')[0].get_text().strip().encode('GBK', 'ignore')
            link = link_head + items[i].select('div[class="title-box"]')[0].a['href'].strip()
            writer.writerow((image1, image2, image3, image4, title, link, 4, category))

    time.sleep(3)


if __name__ == "__main__":
    csvFile = open("crawlnews.csv", 'wb')
    get_news(csvFile, toutiao.URL_RECOMMEND, "recommend")
    get_news(csvFile, toutiao.URL_HOT, "hot")
    get_news(csvFile, toutiao.URL_SOCIETY, "society")
    get_news(csvFile, toutiao.URL_ENTERTAINMENT, "entertainment")
    get_news(csvFile, toutiao.URL_SPORTS, "sports")
    get_news(csvFile, toutiao.URL_FINANCE, "finance")
    get_news(csvFile, toutiao.URL_WORLD, "world")
    get_news(csvFile, toutiao.URL_MILITARY, "military")
    get_news(csvFile, toutiao.URL_TECH, "tech")
    get_news(csvFile, toutiao.URL_CAR, "car")
    get_news(csvFile, toutiao.URL_FUNNY, "funny")
    get_news(csvFile, toutiao.URL_FASHION, "fashion")
    get_news(csvFile, toutiao.URL_TRAVEL, "travel")
