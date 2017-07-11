# coding=utf-8

"""
用于时间戳和日期互相转换转换
"""

import time


def main():
    time1 = 1487138613
    time2 = 1489505204
    print time1 < time2
    timeStamp = 1489505204
    localTime = time.localtime(timeStamp)
    dateTime = time.strftime("%Y-%m-%d %H:%M:%S", localTime)
    print dateTime

    dateTime1 = '2017-02-15 14:03:33'
    timeArray = time.strptime(dateTime1, "%Y-%m-%d %H:%M:%S")
    timeStamp1 = int(time.mktime(timeArray))
    print timeStamp1

if __name__ == '__main__':
    main()

