# -*-coding: utf-8-*-
import logging
from logging.handlers import TimedRotatingFileHandler
import json

import datetime
import requests
import time
import xlrd
import xlwt
from pyquery import PyQuery as pq
from scrapy.scrapy import scrapy
import threading
from utils.threadpool import ThreadPool


# createTime: 2017-10-09 12:02:33
# desc: 深圳证券交易所相关数据下载


def config_log():
    fmt = '%(asctime)s - %(threadName)s - %(levelname)s - %(message)s'
    log = logging.getLogger('')
    fileTimeHandler = TimedRotatingFileHandler('../../log/SZZQScrapy.log', "D", 1, 3)
    fileTimeHandler.suffix = "%Y%m%d"
    fileTimeHandler.setFormatter(logging.Formatter(fmt))
    logging.basicConfig(level=logging.DEBUG, format=fmt)
    log.addHandler(fileTimeHandler)


class SZZQScrapy():
    def __init__(self):
        super(SZZQScrapy, self).__init__()
        self.session = requests.session()
        self.timeout = 15

    def search(self):
        return None

    def parseResponse(self):
        return None

    def main(self, search_key):
        index = 1
        while True:
            resultStr = self.search(search_key, index)
            if resultStr == None:
                return None
            data_list = self.parseResponse(resultStr, search_key)
            if data_list == []:
                break
            self.xlsWrite(data_list, 'SHZQ', 'shzq_demo.xls')
            index += 1
        return None


if __name__ == '__main__':
    config_log()
    result = SZZQScrapy()
    search_data = ['问询函', '关注函']
    for x in search_data:
        result.main(x)