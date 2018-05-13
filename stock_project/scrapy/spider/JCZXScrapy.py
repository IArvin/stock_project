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


# createTime: 2017-9-28 11:52:41
# desc: 巨潮资讯相关数据下载


def config_log():
    fmt = '%(asctime)s - %(threadName)s - %(levelname)s - %(message)s'
    log = logging.getLogger('')
    fileTimeHandler = TimedRotatingFileHandler('../../log/JCZXScrapy.log', "D", 1, 3)
    fileTimeHandler.suffix = "%Y%m%d"
    fileTimeHandler.setFormatter(logging.Formatter(fmt))
    logging.basicConfig(level=logging.DEBUG, format=fmt)
    log.addHandler(fileTimeHandler)


class JCZXScrapy(scrapy):
    def __init__(self):
        super(JCZXScrapy, self).__init__()
        self.session = requests.session()
        self.timeout = 12

    def search(self, search_key, index):
        if index == 7:
            print('lllllll')
        logging.info('index is: %s' % str(index))
        params = {
            "searchkey": search_key,
            "sdate": "",
            "edate": "",
            "isfulltext": "false",
            "sortName": "nothing",
            "sortType": "desc",
            "pageNum": "%s" % str(index)
        }
        search_page = {}
        try:
            self.session.get('http://www.cninfo.com.cn/cninfo-new/index', timeout=self.timeout)
            search_page = self.session.get('http://www.cninfo.com.cn/cninfo-new/fulltextSearch/full', params=params, timeout=self.timeout).json()
            print(json.dumps(search_page))
        except Exception, e:
            logging.info(e)

        if search_page == {}:
            logging.info('search data failed...')
            return {}
        return search_page

    def parseRespone(self, search_page, search_key):
        logging.info(json.dumps(search_page))
        if search_page['announcements'] == []:
            return []
        data_list = []
        url = 'http://www.cninfo.com.cn/'
        for tr in search_page['announcements']:
            judge_time = datetime.datetime.strptime('2017-09-30', '%Y-%m-%d')
            now_file_time = datetime.datetime.strptime(tr['adjunctUrl'].split('/')[-2], '%Y-%m-%d')
            if now_file_time > judge_time:
                continue

            data_dict = {}
            data_dict['company_name'] = tr['secName']
            data_dict['title'] = tr['announcementTitle']
            data_dict['stock_id'] = tr['secCode']
            data_dict['file_size'] = str(tr['adjunctSize'])+'KB'
            data_dict['time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(str(tr['announcementTime'])[:-3])))
            self.savePDF(tr['adjunctUrl'], tr['secCode'], search_key, url, 'JCZX', tr['adjunctUrl'].split('/')[-2])
            data_list.append(data_dict)
        return data_list

    def main(self, data):
        index = 1
        while True:
            response_dict = self.search(data, index)
            if response_dict == {}:
                continue
            data_list = self.parseRespone(response_dict, data)
            if data_list == []:
                break

            if data == '年报问询':
                excel_file_name = 'jczx_attention_demo.xls'
            else:
                excel_file_name = 'jczx_inquiry_demo.xls'

            self.xlsWrite(data_list, 'JCZX', excel_file_name, data)
            index += 1
        return None

    def run(self):
        search_data = ['年报问询', '年报回函']
        for data in search_data:
            index = 1
            while True:
                response_dict = self.search(data, index)
                if response_dict == {}:
                    continue
                data_list = self.parseRespone(response_dict, data)
                if data_list == []:
                    break

                if data == '年报问询':
                    excel_file_name = 'jczx_attention_demo.xls'
                else:
                    excel_file_name = 'jczx_inquiry_demo.xls'

                self.xlsWrite(data_list, 'JCZX', excel_file_name, data)
                index += 1


if __name__ == '__main__':
    config_log()
    result = JCZXScrapy()
    search_data = ['年报问询', '年报回函']
    for x in search_data:
        result.main(x)
