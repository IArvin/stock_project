# -*-coding:utf-8-*-
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


# createTime: 2018-04-21 12:18:41
# desc: 国内首家上市公司社会责任专业评测2010-2016数据下载


def config_log():
    fmt = '%(asctime)s - %(threadName)s - %(levelname)s - %(message)s'
    log = logging.getLogger('')
    fileTimeHandler = TimedRotatingFileHandler('../../log/CEScrapy.log', "D", 1, 3)
    fileTimeHandler.suffix = "%Y%m%d"
    fileTimeHandler.setFormatter(logging.Formatter(fmt))
    logging.basicConfig(level=logging.DEBUG, format=fmt)
    log.addHandler(fileTimeHandler)


class CEScrapy(scrapy):
    def __init__(self):
        super(CEScrapy, self).__init__()
        self.session = requests.session()
        self.timeout = 10

    def search(self):
        self.session.get('')
        return None