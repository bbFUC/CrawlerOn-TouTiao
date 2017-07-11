



import oss2
# import requests


auth = oss2.Auth("LTAI0v7wW5zXRoji", 'MdICV5A7wODPFlIHcrWfUmt8yKbtQt')
bucket = oss2.Bucket(auth, "http://oss-cn-beijing.aliyuncs.com", 'tju-toutiao')

# a = requests.get('https://imgsa.baidu.com/baike/c0%3Dbaike180%2C5%2C5%2C180%2C60/sign=ca5abb5b7bf0f736ccf344536b3cd87c/29381f30e924b899c83ff41c6d061d950a7bf697.jpg')

# bucket.put_object('cccc', a.content, headers={'Content-Type': "image/jpeg"})
# bucket.put

s = '1333213' + '/'
bucket.put_object(s, '')
bucket.put_object('liwexi/li/', '')
bucket.put_object('remote.txt', 'local.txt')

