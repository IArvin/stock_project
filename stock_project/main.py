# -*-coding: utf-8-*-
import logging
from logging.handlers import TimedRotatingFileHandler
import thread
import threading
import time
import os
from scrapy.spider.JCZXScrapy import JCZXScrapy
from scrapy.spider.SHZQScrapy import SHZQScrapy
from scrapy.spider.SZZQScrapy import SZZQScrapy
from scrapy.spider.XLSScrapy import XLSScrapy


# The project is spider project
# which is used to crawl data on several securities sites.
# The project is only for learning and not for commercial use.


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
        jczx = JCZXScrapy()
        jczx.start()
        shzq = SHZQScrapy()
        shzq.start()
        szzq = SZZQScrapy()
        szzq.start()
        xlsx = XLSScrapy()
        xlsx.start()


if __name__ == '__main__':
    config_log()
    logging.info('global setting init ......')
    stock = stockEngine()
    stock.main()
