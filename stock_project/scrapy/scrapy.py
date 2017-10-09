# -*-coding: utf-8-*-
import logging
from logging.handlers import TimedRotatingFileHandler
from xlutils.copy import copy
import os
import xlwt
import xlrd
from xlrd import open_workbook
from xlwt import *

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


class scrapy(object):
    def __init__(self):
        pass

    def savePDF(self, pdf_url, stock_id, search_key, url, judge, file_time):
        pdf_response = ''
        try:
            pdf_response = self.session.get(url+pdf_url, timeout=PDF_REQUESTS_TIMEOUT)
        except Exception, e:
            logging.info(e)
        if pdf_response == '':
            logging.info('request failed, no response, return None')
            return 'failed'

        path = ''

        if search_key == '关注函':
            path = '../../download_file/attention/'+ BRANCH_DICT[judge]
        elif search_key == '问询函':
            path = '../../download_file/inquiry/'+ BRANCH_DICT[judge]
        else:
            return ''

        pdf_name = path + stock_id + '_' + file_time + '.PDF'

        if pdf_name == '':
            return None
        f = open(pdf_name, 'wb')
        f.write(pdf_response.content)
        f.close()
        logging.info('save success, return ...')
        return 'success'

    def write_excel(self, data_list, website):
        excel = xlwt.Workbook()
        sheet01 = excel.add_sheet('demo_01')
        for index, tr in enumerate(data_list):
            sheet01.write(index, 0, tr['company_name'])
            sheet01.write(index, 1, tr['title'])
            sheet01.write(index, 2, tr['stock_id'])
            sheet01.write(index, 3, tr['file_size'])
            sheet01.write(index, 4, tr['time'])
        if website == 'JCZX':
            excel.save('../../download_file/excel_file/jczx_demo.xls')
        elif website == 'SHZQ':
            excel.save('../../download_file/excel_file/shzq_demo.xls')
        logging.info('save excel file success!')

    def xlsWrite(self, data_list, website, file_name):
        writeInfo = '../../download_file/excel_file/'
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
                        ws.write(index+nrows, 0, tr['company_name'])
                        ws.write(index+nrows, 1, tr['title'])
                        ws.write(index+nrows, 2, tr['stock_id'])
                        ws.write(index+nrows, 3, tr['file_size'])
                        ws.write(index+nrows, 4, tr['time'])
                    os.remove(writeInfo + file_name)
                    wb.save(writeInfo + file_name)
                    logging.info('write in success!')
                    break
            else:
                self.write_excel(data_list, website)
        else:
            self.write_excel(data_list, website)

if __name__ == '__main__':
    res = scrapy()
    res.xlsWrite([], 'SHZQ', 'shzq_demo.xls')