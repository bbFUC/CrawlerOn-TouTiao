# coding=utf-8

"""
对MongoDB的连接进行简单包装，以后有需求可以往里加
"""
from mylog import get_logger
from mongoengine import *
from config import mod_config


"""
如主页推荐一般形式的新闻储存(今日头条中大多数新闻界面都是这个形式)
需要把新闻的某些条目作为索引提取出来可在此处进行修改
"""
class RecommendTypedNewsEngine(Document):
    group_id = StringField(required=True, unique=True)
    news_tag = StringField(unique=False)    # 新闻类型
    comment_count = IntField(unique=False)  # 评论数
    behot_time = IntField(unique=False)     # 新闻时间
    ori_data = DictField(required=True)     # 其余项
    meta = {'collection': mod_config.get_config('mongodb', 'collection')}

    @classmethod
    def create_regular_obj(cls, ori_data):
        try:
            cls(group_id=ori_data['group_id'], news_tag=ori_data['tag'], comment_count=ori_data['comments_count'], behot_time=ori_data['behot_time'], ori_data=ori_data).save()

        except Exception as e:
            print "news object save error: ", e
            s = str(e)
            mongoDBControllerErrorMessage = get_logger('mongoDBController.log')
            mongoDBControllerErrorMessage.error('recommend-typed news object save error: ' + s)

    @classmethod
    def check_regular_obj(cls, ori_data):
        obj = cls.objects(group_id=ori_data['group_id']).first()

        if obj:
            return True
        else:
            return False

"""
段子类新闻的储存
"""
class JokeNewsEngine(Document):
    id_str = StringField(required=True, unique=True)
    favorite_count = IntField(required=True)  # 收藏数
    go_detail_count = IntField(required=True)  # 点击量
    comment_count = IntField(required=True)  # 评论数
    share_count = IntField(required=True)  # 分享数
    bury_count = IntField(required=True)  # 不喜欢数
    digg_count = IntField(required=True)  # 喜欢数
    online_time = IntField(required=True)  # 时间戳
    ori_data = DictField(required=True)
    meta = {'collection': mod_config.get_config('mongodb', 'collection')}

    @classmethod
    def create_joke_obj(cls, ori_data):
        try:
            cls(id_str=ori_data['group']['id_str'], favorite_count=ori_data['group']['favorite_count'], comment_count=ori_data['group']['comment_count'], go_detail_count=ori_data['group']['go_detail_count'],
                share_count=ori_data['group']['share_count'], bury_count=ori_data['group']['bury_count'], digg_count=ori_data['group']['digg_count'], online_time=ori_data['online_time'], ori_data=ori_data).save()

        except Exception as e:
            print "news object save error: ", e
            s = str(e)
            mongoDBControllerErrorMessage = get_logger('mongoDBController.log')
            mongoDBControllerErrorMessage.error('joke news object save error: ' + s)

    # 检查此新闻数据库里面是否已经存在
    @classmethod
    def check_joke_obj(cls, ori_data):
        obj = cls.objects(id_str=ori_data['group']['id_str']).first()

        if obj:
            return True
        else:
            return False


class MongoDBController():
    def __init__(self, dataBase, host, port):
        self.dataBase = dataBase
        self.host = host
        self.port = port

    def connectToMongoDB(self):
        try:
            connect(self.dataBase, host=self.host, port=self.port)

        except Exception as e:
            print 'connect to MongoDB error', e
            s = str(e)
            MongoDBControllerConnectionErrorMessage = get_logger('MongoDBController.log')
            MongoDBControllerConnectionErrorMessage.error('mongoDB connection error: ' + s)
