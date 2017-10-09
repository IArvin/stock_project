# -*-coding: utf-8-*-
import logging
from logging.handlers import TimedRotatingFileHandler

from scrapy.spider.JCZXScrapy import JCZXScrapy
from scrapy.spider.SHZQScrapy import SHZQScrapy


def config_log():
    fmt = '%(asctime)s - %(threadName)s - %(levelname)s - %(message)s'
    log = logging.getLogger('')
    fileTimeHandler = TimedRotatingFileHandler('main.log', "D", 1, 3)
    fileTimeHandler.suffix = "%Y%m%d"
    fileTimeHandler.setFormatter(logging.Formatter(fmt))
    logging.basicConfig(level=logging.DEBUG, format=fmt)
    log.addHandler(fileTimeHandler)


def main():
    JCZX_result = JCZXScrapy()
    SHZQ_result = SHZQScrapy()
    search_data = ['关注函', '问询函']
    for x in search_data:
        JCZX_result.main(x)
        SHZQ_result.main(x)


if __name__ == '__main__':
    config_log()
    main()