# -*- coding: UTF-8 -*-
import time
import re

from selenium import webdriver
from bs4 import BeautifulSoup
from pathlib import Path
from urllib import request

import constant.toutiao as toutiao


def get_timestamp():
    """
    获取当前时间
    """
    row_timestamp = str(time.strftime("%a %b %d %H:%M:%S %Y", time.localtime()))
    return row_timestamp

def create_dir(name):
    """
    根据传入的目录名创建一个目录，这里用到了 python3.4 引入的 pathlib 库。
    """
    directory = Path(name)
    if not directory.exists():
        directory.mkdir()
    return directory

def save_photo(photo_url, save_dir, timeout=10):
    photo_name = photo_url.rsplit('/', 1)[-1] + '.jpg'

    # 这是 pathlib 的特殊操作，其作用是将 save_dir 和 photo_name 拼成一个完整的路径。例如：
    # save_dir = 'C：\news'
    # photo_name = '13f000065b3a357999bd.jpg'
    # 则 save_path = 'C：\news\13f000065b3a357999bd.jpg'
    save_path = save_dir / photo_name

    with request.urlopen(photo_url, timeout=timeout) as res, save_path.open('wb') as f:
        f.write(res.read())


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

def get_news(url, category):
    link_head = 'https://toutiao.com'
    soup = BeautifulSoup(get_page(url), "html.parser")
    items = soup.find_all("div", {"class": "item-inner"})
    #newsTime = get_timestamp().replace(':', '-')


    #新闻个数
    print (u"items的数量是:", len(items))
    #获取新闻题目链接和图片链接
    for i in range(0, len(items)):
        if len(items[i].select('img')) == 0:
            print ('0')
            title = items[i].select('div[class="title-box"]')[0].get_text().strip()
            link = link_head + items[i].select('div[class="title-box"]')[0].a['href'].strip()
            dir_name = re.sub(r'[\\/:*?"<>|]', '', title) 
            root_dir = create_dir('C:\\news') 
            root_dir = create_dir(root_dir / newsTime) # 保存图片的根目录
            download_dir = create_dir(root_dir / dir_name)

        elif len(items[i].select('img')) == 1:
            print ('1')
            image = items[i].select('img')[0].get('src')
            title = items[i].select('div[class="title-box"]')[0].get_text().strip()
            link = link_head + items[i].select('div[class="title-box"]')[0].a['href'].strip()
            dir_name = re.sub(r'[\\/:*?"<>|]', '', title)
            root_dir = create_dir('C:\\news')  # 保存图片的根目录
            root_dir = create_dir(root_dir / newsTime) # 保存图片的根目录
            download_dir = create_dir(root_dir / dir_name)
            save_photo(image, save_dir=download_dir)

        elif len(items[i].select('img')) == 2:
            print ('2')
            image1 = items[i].select('img')[0].get('src')
            image2 = items[i].select('img')[1].get('src')
            title = items[i].select('div[class="title-box"]')[0].get_text().strip()
            link = link_head + items[i].select('div[class="title-box"]')[0].a['href'].strip()
            dir_name = re.sub(r'[\\/:*?"<>|]', '', title)
            root_dir = create_dir('C:\\news')  # 保存图片的根目录
            root_dir = create_dir(root_dir / newsTime) # 保存图片的根目录
            download_dir = create_dir(root_dir / dir_name)
            save_photo(image1, save_dir=download_dir)
            save_photo(image2, save_dir=download_dir)

        elif len(items[i].select('img')) == 3:
            print ('3')
            image1 = items[i].select('img')[0].get('src')
            image2 = items[i].select('img')[1].get('src')
            image3 = items[i].select('img')[2].get('src')
            title = items[i].select('div[class="title-box"]')[0].get_text().strip()
            link = link_head + items[i].select('div[class="title-box"]')[0].a['href'].strip()
            dir_name = re.sub(r'[\\/:*?"<>|]', '', title)
            root_dir = create_dir('C:\\news')  # 保存图片的根目录
            root_dir = create_dir(root_dir / newsTime) # 保存图片的根目录
            download_dir = create_dir(root_dir / dir_name)
            save_photo(image1, save_dir=download_dir)
            save_photo(image2, save_dir=download_dir)
            save_photo(image3, save_dir=download_dir)

        else:
            print ('4')
            image1 = items[i].select('img')[0].get('src')
            image2 = items[i].select('img')[1].get('src')
            image3 = items[i].select('img')[2].get('src')
            image4 = items[i].select('img')[3].get('src')
            title = items[i].select('div[class="title-box"]')[0].get_text().strip()
            link = link_head + items[i].select('div[class="title-box"]')[0].a['href'].strip()
            dir_name = re.sub(r'[\\/:*?"<>|]', '', title)
            root_dir = create_dir('C:\\news')  # 保存图片的根目录
            root_dir = create_dir(root_dir / newsTime) # 保存图片的根目录
            download_dir = create_dir(root_dir / dir_name)
            save_photo(image1, save_dir=download_dir)
            save_photo(image2, save_dir=download_dir)
            save_photo(image3, save_dir=download_dir)
            save_photo(image4, save_dir=download_dir)

    time.sleep(3)


if __name__ == "__main__":
    newsTime = get_timestamp().replace(':', '-')
    get_news(toutiao.URL_RECOMMEND, "recommend")
    get_news(toutiao.URL_HOT, "hot")
    get_news(toutiao.URL_SOCIETY, "society")
    get_news(toutiao.URL_ENTERTAINMENT, "entertainment")
    get_news(toutiao.URL_SPORTS, "sports")
    get_news(toutiao.URL_FINANCE, "finance")
    get_news(toutiao.URL_WORLD, "world")
    get_news(toutiao.URL_MILITARY, "military")
    get_news(toutiao.URL_TECH, "tech")
    get_news(toutiao.URL_CAR, "car")
    get_news(toutiao.URL_FUNNY, "funny")
    get_news(toutiao.URL_FASHION, "fashion")
    get_news(toutiao.URL_TRAVEL, "travel")
