# -*-coding: utf-8-*-
import logging
from logging.handlers import TimedRotatingFileHandler
import thread
import threading
import time
from scrapy.spider.JCZXScrapy import JCZXScrapy
from scrapy.spider.SHZQScrapy import SHZQScrapy
from scrapy.spider.SZZQScrapy import SZZQScrapy
from scrapy.spider.XLSScrapy import XLSScrapy


def config_log():
    fmt = '%(asctime)s - %(threadName)s - %(levelname)s - %(message)s'
    log = logging.getLogger('')
    fileTimeHandler = TimedRotatingFileHandler('stockEngine.log', "D", 1, 3)
    fileTimeHandler.suffix = "%Y%m%d"
    fileTimeHandler.setFormatter(logging.Formatter(fmt))
    logging.basicConfig(level=logging.DEBUG, format=fmt)
    log.addHandler(fileTimeHandler)


class stockEngine(object):
    def __init__(self):
        pass

    def main(self):
        search_data = ['关注函', '问询函']
        jczx = JCZXScrapy()
        jczx.start()
        # for x in search_data:
        #     pass

if __name__ == '__main__':
    print 'hello world!'
    config_log()
    stock = stockEngine()
    stock.main()
    while True:
        time.sleep(5)