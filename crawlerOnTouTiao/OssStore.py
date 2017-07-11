# coding=utf-8

"""
这个模块用来将新闻中图片储存到oss云端
"""
import oss2
import requests
from config import mod_config


class OssStore():
    def __init__(self):
        self.bucket_name = mod_config.get_config('aliyun_oss', 'bucket_name')
        self.access_key = mod_config.get_config('aliyun_oss', 'access_key')
        self.access_secret_key = mod_config.get_config('aliyun_oss', 'access_secret_key')
        self.http_prefix = mod_config.get_config('aliyun_oss', 'http_prefix')
        self.auth = oss2.Auth(self.access_key, self.access_secret_key)
        self.bucket = oss2.Bucket(self.auth, self.http_prefix, self.bucket_name)

    def save_image_in_oss(self, url, newsType, newsTime, newsTitle, count):
        img = requests.get(url)
        # # 进入新闻类型的文件夹
        # newsType = str(newsType) + '/'
        # # 进入时间戳文件夹
        # newsTime = newsType + str(newsTime) + '/'
        # # 进入新闻标题文件夹
        # newsTitle = newsTime + str(newsTitle) + '/'
        # # 给图片命名
        # nameOfImage = newsTitle + str(count) + '.jpg'
        # # 上传图片

        # 进入时间戳文件夹
        newsTime = str(newsTime) + '/'
        # 进入新闻类型的文件夹
        newsType = newsTime + str(newsType) + '/'
        # 进入新闻标题文件夹
        newsTitle = newsType + str(newsTitle) + '/'
        # 给图片命名
        nameOfImage = newsTitle + str(count) + '.jpg'
        # 上传图片
        self.bucket.put_object(nameOfImage, img.content, headers={'Content-Type': "image/jpeg"})
