# -*-coding: utf-8-*-
import logging
import os
from logging.handlers import TimedRotatingFileHandler
import json
from xlutils.copy import copy
import datetime
import requests
from xlrd import open_workbook
import time
import xlrd
import xlwt
from pyquery import PyQuery as pq
from scrapy.scrapy import scrapy
import threading
from utils.threadpool import ThreadPool


# createTime: 2017-10-09 16:02:05
# desc: EXCEL表单中问询公告相关数据下载


class XLSScrapy():
    def __init__(self):
        self.session = requests.session()
        self.timeout = 15

    def read_excel(self):
        book = xlrd.open_workbook("../../tools/notice_inquiry.xls", formatting_info=True)
        sheet = book.sheets()[0]
        nrows = sheet.nrows

        data_list = []
        for nrow in xrange(1, nrows):
            data_dict = {}
            data_dict['announcement_time'] = sheet.cell(nrow, 0).value
            data_dict['stock_id'] = sheet.cell(nrow, 1).value
            data_dict['announcement_title'] = sheet.cell(nrow, 2).value
            data_dict['url'] = sheet.cell(nrow, 3).value
            data_list.append(data_dict)
        return data_list

    def search(self, data_list):
        announcement_list = []
        for index, tr in enumerate(data_list):
            logging.info('index is: %s' % str(index))
            announcement_dict = {}
            response = ''
            try:
                response = self.session.get(tr['url'], timeout=self.timeout)
            except Exception, e:
                logging.info(e)
            if response == '' or response.status_code != 200:
                continue

            b = pq(response.content)
            announcement_dict['title'] = b('div[id="snapTitle"]').text()
            time_html = b('form[id="form1"] div:eq(1)').html()
            if u'公告日期' in time_html:
                announcement_dict['announcement_time'] = time_html.split('\t')[-1].replace(' ', '').encode('utf-8')
            else:
                announcement_dict['announcement_time'] = ''
            announcement_dict['stock_id'] = tr['stock_id'].split('.')[0]
            pdf_label_url = b('form[id="form1"] div:eq(2) a').attr('href')
            self.savePDF(pdf_label_url, announcement_dict['announcement_time'], announcement_dict['stock_id'])
            logging.info(b('form[id="form1"] div:eq(2) div:eq(1)').text().split(' ('))
            announcement_dict['pdf_label'] = [tr for tr in b('form[id="form1"] div:eq(2) div:eq(1)').text().split(' (') if '.pdf' in tr]
            # print b('form[id="form1"] div:eq(2) div:eq(1)').text().split(' ')
            announcement_dict['file_size'] = b('form[id="form1"] div:eq(2) div:eq(1)').text().split(' ')[-2] if len(b('form[id="form1"] div:eq(2) div:eq(1)').text().split(' ')) >= 2 else ''
            announcement_list.append(announcement_dict)
            if len(announcement_list) == 10 or index == len(data_list)-1:
                self.writeXLS(announcement_list, 'announcement.xls')
                announcement_list = []
        return None

    def savePDF(self, pdf_url, announcement_time, stock_id):
        url = 'http://news.windin.com/ns/'
        response = ''
        try:
            response = self.session.get(url+pdf_url, timeout=self.timeout)
        except Exception, e:
            logging.info(e)
        if response == '' or response.status_code != 200:
            return None

        path = '../../download_file/announcement/pdf/'

        pdf_name = path + stock_id + '_' + announcement_time + '.PDF'
        if pdf_name == '':
            return None
        f = open(pdf_name, 'wb')
        f.write(response.content)
        f.close()
        logging.info('save pdf file success, return ...')
        return 'success'

    def writeXLS(self, announcement_list, file_name):
        writeInfo = '../../download_file/announcement/'
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
                    for index, tr in enumerate(announcement_list):
                        ws.write(index + nrows, 0, tr['pdf_label'])
                        ws.write(index + nrows, 1, tr['title'])
                        ws.write(index + nrows, 2, tr['stock_id'])
                        ws.write(index + nrows, 3, tr['file_size'])
                        ws.write(index + nrows, 4, tr['announcement_time'])
                    os.remove(writeInfo + file_name)
                    wb.save(writeInfo + file_name)
                    logging.info('write in success!')
                    break
            else:
                self.write_excel(announcement_list, file_name)
        else:
            self.write_excel(announcement_list, file_name)
        return None

    def write_excel(self, announcement_list, file_name):
        excel = xlwt.Workbook()
        sheet01 = excel.add_sheet('demo_01')
        for index, tr in enumerate(announcement_list):
            sheet01.write(index, 0, tr['pdf_label'])
            sheet01.write(index, 1, tr['title'])
            sheet01.write(index, 2, tr['stock_id'])
            sheet01.write(index, 3, tr['file_size'])
            sheet01.write(index, 4, tr['announcement_time'])
        excel.save('../../download_file/announcement/'+file_name)
        logging.info('save excel file success!')

    def main(self):
        data_list = self.read_excel()
        self.search(data_list)
        return None


def config_log():
    fmt = '%(asctime)s - %(threadName)s - %(levelname)s - %(message)s'
    log = logging.getLogger('')
    fileTimeHandler = TimedRotatingFileHandler('../../log/XLSScrapy.log', "D", 1, 3)
    fileTimeHandler.suffix = "%Y%m%d"
    fileTimeHandler.setFormatter(logging.Formatter(fmt))
    logging.basicConfig(level=logging.DEBUG, format=fmt)
    log.addHandler(fileTimeHandler)


if __name__ == '__main__':
    config_log()
    res = XLSScrapy()
    res.main()