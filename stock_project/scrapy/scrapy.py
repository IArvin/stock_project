# -*-coding: utf-8-*-
import logging
from logging.handlers import TimedRotatingFileHandler
from xlutils.copy import copy
import os
import xlwt
import xlrd
from xlrd import open_workbook
from xlwt import *
import threading

PDF_REQUESTS_TIMEOUT = 10
BRANCH_DICT = {'JCZX': 'JCZX_file/', 'SHZQ': 'SHZQ_file/', 'SZZQ': 'SZZQ_file/'}


# createTime: 2017-10-06 18:31:24
# desc: spider public method


def config_log():
    fmt = '%(asctime)s - %(threadName)s - %(levelname)s - %(message)s'
    log = logging.getLogger('')
    fileTimeHandler = TimedRotatingFileHandler('../log/JCZXScrapy.log', "D", 1, 3)
    fileTimeHandler.suffix = "%Y%m%d"
    fileTimeHandler.setFormatter(logging.Formatter(fmt))
    logging.basicConfig(level=logging.DEBUG, format=fmt)
    log.addHandler(fileTimeHandler)


class scrapy(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def savePDF(self, pdf_url, stock_id, search_key, url, judge, file_time):
        pdf_response = ''
        try:
            pdf_response = self.session.get(url + pdf_url, timeout=PDF_REQUESTS_TIMEOUT)
        except Exception, e:
            logging.info(e)
        if pdf_response == '':
            logging.info('request failed, no response, return None')
            return 'failed'

        path = ''

        if search_key == '关注函':
            path = 'download_file/attention/' + BRANCH_DICT[judge]
        elif search_key == '问询函':
            path = 'download_file/inquiry/' + BRANCH_DICT[judge]
        else:
            return ''

        if not os.path.exists(path):
            os.makedirs(path)

        if '_doc' in stock_id:
            pdf_name = path + stock_id.split('_')[0] + '_' + file_time + '.docx'
        else:
            pdf_name = path + stock_id + '_' + file_time + '.PDF'

        if pdf_name == '':
            logging.info('pdf name is null, return ...')
            return ''
        f = open(pdf_name, 'wb')
        f.write(pdf_response.content)
        f.close()
        logging.info('save pdf file success, return ...')
        return 'success'

    def write_excel(self, data_list, website, search_key):
        excel = xlwt.Workbook()
        sheet01 = excel.add_sheet('demo_01')
        for index, tr in enumerate(data_list):
            sheet01.write(index, 0, tr['company_name'])
            sheet01.write(index, 1, tr['title'])
            sheet01.write(index, 2, tr['stock_id'])
            sheet01.write(index, 3, tr['file_size'])
            sheet01.write(index, 4, tr['time'])

        excel_path = 'download_file/excel_file/'

        if not os.path.exists(excel_path):
            os.makedirs(excel_path)

        if website == 'JCZX':
            if search_key == '关注函':
                excel.save(excel_path + 'jczx_attention_demo.xls')
            else:
                excel.save(excel_path + 'jczx_inquiry_demo.xls')
        elif website == 'SHZQ':
            if search_key == '关注函':
                excel.save(excel_path + 'shzq_attention_demo.xls')
            else:
                excel.save(excel_path + 'shzq_inquiry_demo.xls')
        logging.info('save excel file success!')

    def xlsWrite(self, data_list, website, file_name, search_key):
        writeInfo = 'download_file/excel_file/'
        if not os.path.exists(writeInfo):
            os.makedirs(writeInfo)

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
                    for index, tr in enumerate(data_list):
                        ws.write(index + nrows, 0, tr['company_name'])
                        ws.write(index + nrows, 1, tr['title'])
                        ws.write(index + nrows, 2, tr['stock_id'])
                        ws.write(index + nrows, 3, tr['file_size'])
                        ws.write(index + nrows, 4, tr['time'])
                    os.remove(writeInfo + file_name)
                    wb.save(writeInfo + file_name)
                    logging.info('write in success!')
                    break
            else:
                self.write_excel(data_list, website, search_key)
        else:
            self.write_excel(data_list, website, search_key)


def callback():
    res = scrapy()
    res.xlsWrite([], 'SHZQ', 'shzq_demo.xls')


if __name__ == '__main__':
    callback()
