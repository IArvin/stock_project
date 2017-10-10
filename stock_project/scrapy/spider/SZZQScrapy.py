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
import sys


reload(sys)
sys.setdefaultencoding('utf-8')


# createTime: 2017-10-09 12:02:33
# desc: 上海证券交易所相关数据下载


def config_log():
    fmt = '%(asctime)s - %(threadName)s - %(levelname)s - %(message)s'
    log = logging.getLogger('')
    fileTimeHandler = TimedRotatingFileHandler('../../log/SZZQScrapy.log', "D", 1, 3)
    fileTimeHandler.suffix = "%Y%m%d"
    fileTimeHandler.setFormatter(logging.Formatter(fmt))
    logging.basicConfig(level=logging.DEBUG, format=fmt)
    log.addHandler(fileTimeHandler)


class SZZQScrapy(scrapy):
    def __init__(self):
        super(SZZQScrapy, self).__init__()
        self.session = requests.session()
        self.timeout = 15

    def search(self):
        data = {
            "ACTIONID": "7",
            "AJAX": "AJAX - TRUE",
            "CATALOGID": "main_wxhj",
            "tab2PAGENO": "1",
            "TABKEY": "tab1"
        }
        self.session.headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
        self.session.headers['Accept-Encoding'] = 'gzip, deflate'
        self.session.headers['Accept-Language'] = 'zh-CN,zh;q=0.8'
        self.session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
        response = self.session.post('http://www.szse.cn/szseWeb/FrontController.szse?randnum=0.7362621638666007', data=data, timeout=self.timeout)
        b = pq(response.content)
        tr_list = b('table[id="REPORTID_tab1"] tr')
        return (tr_list, b)

    def parseResponse(self, tr_list, b):
        data_list = []
        for index, tr in enumerate(tr_list):
            data_dict = {}
            if index == 0:
                continue
            data_dict['stock_id'] = b('td:first', tr).text()
            print b('td:eq(1)', tr).text()
            data_dict['company_name'] = b('td:eq(1)', tr).text().encode('unicode-escape').decode('string_escape').decode('gbk').encode('utf-8')
            data_dict['attention_time'] = b('td:eq(2)', tr).text()
            data_dict['attention_type'] = b('td:eq(3)', tr).text().encode('unicode-escape').decode('string_escape').decode('gbk').encode('utf-8')
            data_dict['detail_url'] = b('td:eq(4) a', tr).attr('onclick')
            data_dict['company_callback'] = b('td:eq(5)', tr).text().encode('unicode-escape').decode('string_escape').decode('gbk').encode('utf-8')
            if data_dict['company_callback'] != '':
                data_dict['company_callback_url'] = b('td:eq(5) a', tr).attr('onclick')
            else:
                data_dict['company_callback_url'] = ''
            data_list.append(data_dict)
        return data_list

    def write_xls(self, data_list):
        book = xlwt.Workbook()
        sh = book.add_sheet('sheet1')
        for index, tr in enumerate(data_list):
            print type(tr['company_name'])
            sh.write(index, 0, tr['stock_id'])
            sh.write(index, 1, unicode(tr['company_name'], 'utf-8'))
            sh.write(index, 2, tr['attention_time'])
            sh.write(index, 3, unicode(tr['attention_type'], 'utf-8'))
            sh.write(index, 4, tr['detail_url'])
            sh.write(index, 5, unicode(tr['company_callback'], 'utf-8'))
            sh.write(index, 6, tr['company_callback_url'])
        book.save('xlsFile.xls')
        logging.info('write in success!')
        return None

    def main(self):
        index = 1
        while True:
            resultStr, b = self.search()
            if resultStr == None:
                return None
            data_list = self.parseResponse(resultStr, b)
            print json.dumps(data_list)
            self.write_xls(data_list)
            # if data_list == []:
            #     break
            # self.xlsWrite(data_list, 'SHZQ', 'shzq_demo.xls')
            index += 1
        return None


if __name__ == '__main__':
    config_log()
    result = SZZQScrapy()
    result.main()