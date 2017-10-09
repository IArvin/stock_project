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


# createTime: 2017-10-06 15:07:33
# desc: 上海证券交易所相关数据下载

def config_log():
    fmt = '%(asctime)s - %(threadName)s - %(levelname)s - %(message)s'
    log = logging.getLogger('')
    fileTimeHandler = TimedRotatingFileHandler('../../log/SHZQScrapy.log', "D", 1, 3)
    fileTimeHandler.suffix = "%Y%m%d"
    fileTimeHandler.setFormatter(logging.Formatter(fmt))
    logging.basicConfig(level=logging.DEBUG, format=fmt)
    log.addHandler(fileTimeHandler)


class SHZQScrapy(scrapy):
    def __init__(self):
        super(SHZQScrapy, self).__init__()
        self.session = requests.session()
        self.threadPool = ThreadPool(20)
        self.timeout = 10

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

    def search(self, search_key, index):
        data = {
            "search": "qwjs",
            "jsonCallBack": "jQuery1112036704347904532786_%s000" % str(int(time.time())),
            "page": "%s" % str(index),
            "searchword": "T_L CTITLE T_D E_KEYWORDS T_JT_E likeT_L%sT_RT_R" % search_key,
            "orderby": "-CRELEASETIME",
            "perpage": "10",
            "_": "%s000" % str(int(time.time()))
        }
        if search_key == '关注函':
            self.session.headers['Referer'] = 'http://www.sse.com.cn/home/search/?webswd=%E5%85%B3%E6%B3%A8%E5%87%BD'
        else:
            self.session.headers['Referer'] = 'http://www.sse.com.cn/home/search/?webswd=%E9%97%AE%E8%AF%A2%E5%87%BD'
        response = ''
        try:
            response = self.session.get('http://query.sse.com.cn/search/getSearchResult.do', params=data, timeout=self.timeout)
        except Exception, e:
            logging.info(e)
        if response == '' or response.status_code != 200:
            logging.info('search data failed...')
            return None
        start = response.text.find(data['jsonCallBack']+'(')
        end = response.text.find(")", start)
        resultStr = response.text[start + len(data['jsonCallBack']+'('):end]
        return resultStr

    def parseResponse(self, response, search_key):
        url = 'http://www.sse.com.cn'
        logging.info(response)
        json_data = json.loads(response)
        if json_data['data'] == []:
            return []
        data_list = []
        for tr in json_data['data']:
            data_dict = {}
            judge_time = datetime.datetime.strptime('2017-09-30', '%Y-%m-%d')
            now_file_time = datetime.datetime.strptime(tr['CRELEASETIME'], '%Y-%m-%d')
            if now_file_time > judge_time:
                continue

            data_dict['company_name'] = ''
            data_dict['title'] = tr['CTITLE_TXT']
            data_dict['stock_id'] = tr['CURL'].split('/')[-1].split('_')[0]
            data_dict['file_size'] = tr['FILESIZE']+'byte'
            data_dict['time'] = tr['CRELEASETIME'] + ' ' + tr['CRELEASETIME2']
            self.savePDF(tr['CURL'], tr['CURL'].split('/')[-1].split('_')[0], search_key, url, 'SHZQ', tr['CRELEASETIME'])
            data_list.append(data_dict)
        return data_list


if __name__ == '__main__':
    config_log()
    result = SHZQScrapy()
    search_data = ['问询函', '关注函']
    for x in search_data:
        result.main(x)