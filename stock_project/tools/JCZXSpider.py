# -*-coding: utf-8-*-

# **************************file desc*****************************
import json
import logging
import re
from logging.handlers import TimedRotatingFileHandler
from pyquery import PyQuery as pq
import requests

__author__ = 'arvin'


# createTime : 2018/12/11 14:46
# desc : this is new py file, please write your desc for this file
# ****************************************************************


def config_log():
    level = logging.INFO
    fmt = '%(asctime)s - %(threadName)s - %(levelname)s - %(message)s'
    log = logging.getLogger('')
    fileTimeHandler = TimedRotatingFileHandler('JCZXSpider.log', "D", 1, 3)
    fileTimeHandler.suffix = "%Y%m%d.log"
    fileTimeHandler.setFormatter(logging.Formatter(fmt))
    logging.basicConfig(level=level, format=fmt)
    log.addHandler(fileTimeHandler)


class JCZXSpider(object):
    def __init__(self):
        self.session = requests.session()
        self.timeout = 5
        self.source = 'http://www.cninfo.com.cn/'

    def main(self, stock_code):
        params = {
            "notautosubmit": "",
            "keyWord": stock_code
        }
        self.session.headers['Host'] = 'www.cninfo.com.cn'
        self.session.headers['Referer'] = 'http://www.cninfo.com.cn/new/index'
        self.session.get('http://www.cninfo.com.cn/new/fulltextSearch', params=params, timeout=self.timeout)

        data = {
            "keyWord": stock_code,
            "maxNum": "11"
        }
        response = self.session.post('http://www.cninfo.com.cn/new/information/topSearch/query', data=data,
                                     verify=False, timeout=self.timeout).json()
        logging.info(json.dumps(response))
        if not response:
            return None
        new_json = {}
        # for js in response:
        #     if '股' in js['category']:
        #         new_json = js
        #         break
        new_json = response[0]

        params = {
            "orgId": new_json['orgId'],
            "stockCode": new_json['code']
        }
        self.session.get('http://www.cninfo.com.cn/new/disclosure/stock', params=params, verify=False,
                         timeout=self.timeout)
        index = 1
        while True:
            params = {
                "pageNum": "%s" % index,
                "pageSize": "30",
                "tabName": "fulltext",
                "column": "szse",
                "stock": "%s,%s" % (new_json['code'], new_json['orgId']),
                "searchkey": "",
                "secid": "",
                "plate": "sz",
                "category": "category_ndbg_szsh;",
                "seDate": "2000-01-01 ~ 2018-12-13"
            }
            response = self.session.post('http://www.cninfo.com.cn/new/hisAnnouncement/query', verify=False, data=params, timeout=self.timeout)
            if response.status_code == 200:
                logging.info(json.dumps(response.json()))
                res_list = response.json()['announcements']
                if not res_list:
                    return None
                self.parse(res_list)

            index = index + 1

    def parse(self, res_list):
        for res in res_list:
            if '摘要' in res['announcementTitle']:
                continue

            years = re.findall('[0-9]+', res['announcementTitle'])[0]
            pdf_name = res['secCode'] + '-' + years + '.pdf'
            url = self.source + res['adjunctUrl']
            response = ''
            for x in range(0, 2):
                try:
                    response = self.session.get(url, verify=False, timeout=self.timeout)
                    if response.status_code == 200:
                        break
                except Exception as e:
                    logging.error(e)
                    continue

            if response == '':
                return None

            if '已取消' in res['announcementTitle']:
                path = 'cancel/'
                a = open(path+pdf_name, 'wb')
                a.write(response.content)
                a.close()
            else:
                path = 'content/'
                a = open(path + pdf_name, 'wb')
                a.write(response.content)
                a.close()


def callback():
    config_log()
    index = 1
    # stock_id = '000048'
    while True:
        stock_id = '%06d'%index
        spider = JCZXSpider()
        spider.main(stock_id)
        if index >= 3000:
            index = 300000
        elif index >= 400000:
            index = 600000
        elif index > 604000:
            break
        index = index + 1


if __name__ == '__main__':
    callback()