# -*- coding: utf-8 -*-

import os
import logging


def get_logger(logger_name='root', mode=logging.DEBUG):

    log_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'log')
    if not os.path.exists(log_path):
        os.mkdir(log_path)

    path = os.path.join(log_path, logger_name)
    logger = logging.getLogger(logger_name)

    logger.setLevel(mode)

    fileHandler = logging.FileHandler(path)
    fileHandler.setLevel(mode)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(mode)

    formatter = logging.Formatter('[%(asctime)s %(levelname)s %(filename)s %(lineno)d] %(message)s')
    fileHandler.setFormatter(formatter)
    consoleHandler.setFormatter(formatter)

    logger.addHandler(fileHandler)
    logger.addHandler(consoleHandler)

    return logger


# if __name__ == '__main__':
#     abc = get_logger('abc')

#     abc.warning('1234567')
