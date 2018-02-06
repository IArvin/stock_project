# -*-coding: utf-8-*-
import logging
import os
from logging.handlers import TimedRotatingFileHandler
import json
import datetime
import requests
import time
import xlrd
import xlwt
from pyquery import PyQuery as pq
from scrapy.scrapy import scrapy
from xlutils.copy import copy
import threading
from utils.threadpool import ThreadPool
from xlrd import open_workbook
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

    def search(self, index):
        table_key_list = ["tab1", "tab2", "tab3"]
        all_result_dict = {}
        logging.info('index is: %s' % str(index))
        for table_key in table_key_list:
            if index == 1:
                data = {
                    "ACTIONID": "7",
                    "AJAX": "AJAX - TRUE",
                    "CATALOGID": "main_wxhj",
                    "tab2PAGENO": "%s" % str(index),
                    "TABKEY": table_key
                }
                if table_key == 'tab2':
                    data.update({
                        "tab1PAGENO": "%s" % str(index),
                        "TABKEY": table_key,
                    })
                elif table_key == 'tab3':
                    data.update({
                        "tab1PAGENO": "%s" % str(index),
                        "TABKEY": table_key,
                    })
            else:
                data = {
                    "ACTIONID": "7",
                    "AJAX": "AJAX - TRUE",
                    "CATALOGID": "main_wxhj",
                    "TABKEY": table_key,
                    "%sPAGENO" % table_key: "%s" % str(index),
                    "REPORT_ACTION": "navigate",
                }
                if table_key == 'tab1':
                    data.update({
                        "tab1PAGECOUNT": "45",
                        "tab1RECORDCOUNT": "897",
                    })
                elif table_key == 'tab2':
                    data.update({
                        "tab1PAGECOUNT": "42",
                        "tab1RECORDCOUNT": "826",
                    })
                else:
                    data.update({
                        "tab3PAGECOUNT": "30",
                        "tab3RECORDCOUNT": "584",
                    })
            self.session.headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
            self.session.headers['Accept-Encoding'] = 'gzip, deflate'
            self.session.headers['Accept-Language'] = 'zh-CN,zh;q=0.8'
            self.session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
            response = self.session.post('http://www.szse.cn/szseWeb/FrontController.szse?randnum=0.7362621638666007', data=data, timeout=self.timeout)
            b = pq(response.content)
            tr_list = b('table[id="REPORTID_%s"] tr' % table_key)
            all_result_dict[table_key] = self.parseResponse(b, tr_list, table_key)
        return all_result_dict

    def save_pdf(self, stock_id, attention_time, detail_url, judge_type, table_key):
        index_url = 'http://www.szse.cn'
        logging.info(detail_url)
        logging.info('%s, %s'%(judge_type, table_key))
        url = index_url+detail_url.split("'")[1]+detail_url.split("'")[3]
        pdf_response = ''
        try:
            pdf_response = self.session.get(url, timeout=self.timeout)
        except Exception, e:
            logging.info(e)

        if pdf_response == '':
            logging.info('request failed, no response, return None')
            return 'failed'

        path = ''

        if table_key == 'tab1':
            if judge_type == 'detail':
                path = 'download_file/szzq_file/big/detail/'
            elif judge_type == 'callback':
                path = 'download_file/szzq_file/big/callback/'
        elif table_key == 'tab2':
            if judge_type == 'detail':
                path = 'download_file/szzq_file/middle/detail/'
            elif judge_type == 'callback':
                path = 'download_file/szzq_file/middle/callback/'
        else:
            if judge_type == 'detail':
                path = 'download_file/szzq_file/small/detail/'
            elif judge_type == 'callback':
                path = 'download_file/szzq_file/small/callback/'

        pdf_name = path + stock_id + '_' + attention_time + '.PDF'

        if pdf_name == '':
            logging.info('pdf_name is null string, return failed!')
            return 'failed'

        f = open(pdf_name, 'wb')
        f.write(pdf_response.content)
        f.close()
        logging.info('save pdf file success, return ...')
        return 'success'

    def parseResponse(self, b, tr_list, table_key):
        data_list = []
        for index, tr in enumerate(tr_list):
            data_dict = {}
            if index == 0:
                continue
            data_dict['stock_id'] = b('td:first', tr).text()
            data_dict['company_name'] = b('td:eq(1)', tr).text().encode('unicode-escape').decode(
                'string_escape').decode('gbk').encode('utf-8')
            data_dict['attention_time'] = b('td:eq(2)', tr).text()
            data_dict['attention_type'] = b('td:eq(3)', tr).text().encode('unicode-escape').decode(
                'string_escape').decode('gbk').encode('utf-8')
            data_dict['detail_url'] = b('td:eq(4) a', tr).attr('onclick')
            data_dict['company_callback'] = b('td:eq(5)', tr).text().encode('unicode-escape').decode(
                'string_escape').decode('gbk').encode('utf-8')
            if data_dict['detail_url'] != '' and data_dict['detail_url'] != None:
                self.save_pdf(data_dict['stock_id'], data_dict['attention_time'], data_dict['detail_url'], 'detail', table_key)
            if data_dict['company_callback'] != '':
                data_dict['company_callback_url'] = b('td:eq(5) a', tr).attr('onclick')
                self.save_pdf(data_dict['stock_id'], data_dict['attention_time'], data_dict['company_callback_url'], 'callback', table_key)
            else:
                data_dict['company_callback_url'] = ''
            data_list.append(data_dict)
        return data_list

    def write_xls(self, data_dict, file_name):
        writeInfo = '../../download_file/szzq_file/'
        listFile = os.listdir(writeInfo)
        if listFile != []:
            if file_name in listFile:
                book = open_workbook(writeInfo + file_name, formatting_info=True)
                for index, sheet in enumerate(book.sheets()):
                    if sheet.name != ('demo_01'):
                        continue

                    logging.info('xls have this sheet,get nrows and write in ......')
                    wb = copy(book)
                    ws = wb.get_sheet(index)
                    nrows = sheet.nrows
                    index = 0
                    for tr in data_dict:
                        for value in data_dict[tr]:
                            ws.write(index + nrows, 0, value['stock_id'])
                            ws.write(index + nrows, 1, unicode(value['company_name'], 'utf-8'))
                            ws.write(index + nrows, 2, value['attention_time'])
                            ws.write(index + nrows, 3, unicode(value['attention_type'], 'utf-8'))
                            ws.write(index + nrows, 4, unicode(value['company_callback'], 'utf-8'))
                            ws.write(index + nrows, 5, tr)
                            index += 1
                    os.remove(writeInfo + file_name)
                    wb.save(writeInfo + file_name)
                    logging.info('write in success!')
                    break
            else:
                self.wri_excel(data_dict)
        else:
            self.wri_excel(data_dict)

    def wri_excel(self, data_dict):
        excel = xlwt.Workbook()
        sheet01 = excel.add_sheet('demo_01')
        index = 0
        for tr in data_dict:
            for value in data_dict[tr]:
                sheet01.write(index, 0, value['stock_id'])
                sheet01.write(index, 1, unicode(value['company_name'], 'utf-8'))
                sheet01.write(index, 2, value['attention_time'])
                sheet01.write(index, 3, unicode(value['attention_type'], 'utf-8'))
                sheet01.write(index, 4, unicode(value['company_callback'], 'utf-8'))
                sheet01.write(index, 5, tr)
                index += 1
        excel.save('../../download_file/szzq_file/szzq_detail.xls')
        logging.info('save excel file success!')

    def run(self):
        index = 1
        while True:
            result_dict = self.search(index)
            if result_dict == {}:
                break
            self.write_xls(result_dict, 'szzq_detail.xls')
            index += 1


if __name__ == '__main__':
    config_log()
    result = SZZQScrapy()
    result.main()