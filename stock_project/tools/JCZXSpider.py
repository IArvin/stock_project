# -*-coding: utf-8-*-

# **************************file desc*****************************
import json
import logging
import re
from logging.handlers import TimedRotatingFileHandler
from pyquery import PyQuery as pq
import threading
import requests
import os
import sys

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

OPERATION_FILE_LOCK = threading.Lock()


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
        try:
            self.session.get('http://www.cninfo.com.cn/new/fulltextSearch', params=params, timeout=self.timeout)

            data = {
                "keyWord": stock_code,
                "maxNum": "11"
            }
            response = self.session.post('http://www.cninfo.com.cn/new/information/topSearch/query', data=data, verify=False, timeout=self.timeout).json()
            logging.info(json.dumps(response))
            if not response:
                return None
            new_json = {}
            new_json = response[0]

            params = {
                "orgId": new_json['orgId'],
                "stockCode": new_json['code']
            }
            self.session.get('http://www.cninfo.com.cn/new/disclosure/stock', params=params, verify=False, timeout=self.timeout)
        except Exception as e:
            logging.error(e)
            return None

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
                "seDate": "2000-01-01 ~ 2018-12-17"
            }
            try:
                response = self.session.post('http://www.cninfo.com.cn/new/hisAnnouncement/query', verify=False, data=params, timeout=self.timeout)
                if response.status_code == 200:
                    logging.info(json.dumps(response.json()))
                    res_list = response.json()['announcements']
                    if not res_list:
                        params['column'] = 'fund'
                        params['plate'] = ''
                        params['category'] = 'category_ndbg_jjgg;'
                        response = self.session.post('http://www.cninfo.com.cn/new/hisAnnouncement/query', verify=False, data=params, timeout=self.timeout)
                        logging.info(json.dumps(response.json()))
                        if response.status_code != 200:
                            return None
                        if not response.json()['announcements']:
                            return None
                        res_list = response.json()['announcements']
                    self.parse(res_list)
            except Exception as e:
                logging.error(e)
                return None

            index = index + 1

    def parse(self, res_list):
        for res in res_list:
            logging.info(res['announcementTitle'])
            if '摘要' in res['announcementTitle']:
                continue
            if not re.findall('[0-9]+', res['announcementTitle']):
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

            OPERATION_FILE_LOCK.acquire()
            if '取消' in res['announcementTitle']:
                path = 'cancel/'
                try:
                    cancel_list = os.listdir(path)
                    if pdf_name in cancel_list:
                        logging.info('had the pdf file, return ...')
                        continue

                    a = open(path+pdf_name, 'wb')
                    a.write(response.content)
                    a.close()
                    logging.info('save pdf file success!!!')
                except Exception as e:
                    logging.error(e)
                finally:
                    OPERATION_FILE_LOCK.release()
            else:
                path = 'content/'
                try:
                    content_list = os.listdir(path)
                    if pdf_name in content_list:
                        logging.info('had the pdf file, return ...')
                        continue

                    a = open(path + pdf_name, 'wb')
                    a.write(response.content)
                    a.close()
                    logging.info('save pdf file success!!!')
                except Exception as e:
                    logging.error(e)
                finally:
                    OPERATION_FILE_LOCK.release()


class my_thread(threading.Thread):
    def __init__(self, stockid):
        threading.Thread.__init__(self)
        self.stock_code = stockid

    def run(self):
        spider = JCZXSpider()
        logging.info(self.stock_code)
        spider.main(self.stock_code)



def callback():
    config_log()
    index = 390000
    # stock_id = '000048'
    while True:
        stock_id = '%06d'%index
        thread = my_thread(stock_id)
        thread.start()
        thread.join()
        # spider = JCZXSpider()
        # spider.main(stock_id)
        if index > 400000:
            break
        index = index + 1

        # if index >= 3000:
        #     index = 300000
        # elif index >= 400000:
        #     index = 600000
        # elif index > 604000:
        #     break
        # index = index + 1


if __name__ == '__main__':
    callback()