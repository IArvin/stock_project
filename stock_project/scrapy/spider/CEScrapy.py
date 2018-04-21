# -*-coding:utf-8-*-
import logging
from logging.handlers import TimedRotatingFileHandler
import json
import datetime
import requests
import time
import xlrd
import xlwt
import demjson
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
        com_list = []
        self.session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
        self.session.headers['Referer'] = 'http://stockdata.stock.hexun.com/zrbg/Plate.aspx?date=2016-12-31'
        self.session.headers['Host'] = 'stockdata.stock.hexun.com'
        for x in xrange(1, 180):
            response = self.session.get('http://stockdata.stock.hexun.com/zrbg/data/zrbList.aspx?date=2016-12-31&count=20&pname=20&titType=null&page=%s&callback=hxbase_json11524298566134'%str(x), timeout=self.timeout, verify=False)
            res = demjson.decode(response.text.replace('hxbase_json1(', '')[0:-1].encode('utf-8'))
            for tr in res['list']:
                logging.info(json.dumps(tr))
                com_list.append(self.parse(tr))
        self.write_xls(com_list)

    def write_xls(self, com_list):
        excel = xlwt.Workbook()
        sheet01 = excel.add_sheet('2016')
        for index, tr in enumerate(com_list):
            sheet01.write(index, 0, tr['company'])
            sheet01.write(index, 1, tr['stockNumber'])
            sheet01.write(index, 2, tr['industryrate'])
            sheet01.write(index, 3, tr['Pricelimit'])
            sheet01.write(index, 4, tr['lootingchips'])
            sheet01.write(index, 5, tr['Scramble'])
            sheet01.write(index, 6, tr['rscramble'])
            sheet01.write(index, 7, tr['Strongstock'])
        excel.save('2016.xls')

    def parse(self, response):
        company_detail = {}
        company_detail['company'] = response['industry']
        company_detail['stockNumber'] = response['stockNumber']
        company_detail['industryrate'] = response['industryrate']
        company_detail['Pricelimit'] = response['Pricelimit']
        company_detail['lootingchips'] = response['lootingchips']
        company_detail['Scramble'] = response['Scramble']
        company_detail['rscramble'] = response['rscramble']
        company_detail['Strongstock'] = response['Strongstock']
        return company_detail


if __name__ == '__main__':
    config_log()
    res = CEScrapy()
    res.search()