# -*- coding: utf-8 -*-

import ConfigParser
import os


def get_config(section, key):
    config = ConfigParser.ConfigParser()
    path = os.path.split(os.path.realpath(__file__))[0] + '/conf.ini'
    config.read(path)
    return config.get(section, key)


def get_config_obj():
    config = ConfigParser.ConfigParser()
    path = os.path.split(os.path.realpath(__file__))[0] + '/conf.ini'
    config.read(path)
    return config


if __name__ == '__main__':
    # print get_config('mongodb', 'port')
    #
    # print repr(get_config('aliyun_oss', 'bucket_name'))
    # print repr(get_config('aliyun_oss', 'access_key'))
    # print repr(get_config('aliyun_oss', 'access_secret_key'))
    # print repr(get_config('aliyun_oss', 'roleam'))
    # print repr(get_config('aliyun_oss', 'callback_url'))

    a = get_config('aliyun_sms', "sign_name")
    b = a.decode('utf-8')

    print a, type(a), b, type(b)
