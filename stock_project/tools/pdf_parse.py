# -*-coding: utf-8-*-

# **************************file desc*****************************
import json
import logging
import os
import subprocess
import sys
# from tabula.wrapper import read_pdf, convert_into
from logging.handlers import TimedRotatingFileHandler
import threading
import xlwt
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBoxHorizontal
# from pdfminer.pdfdocument import PDFDocument, PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter, PDFTextExtractionNotAllowed
from pdfminer.pdfparser import PDFParser, PDFDocument
from PyPDF2 import PdfFileReader
from utils.threadpool import ThreadPool
from tabula.wrapper import read_pdf
import platform

__author__ = 'arvin'
# createTime : 2019/1/2 14:24
# desc : this is new py file, please write your desc for this file
# ****************************************************************

DATABASE_LOCK = threading.Lock()

def config_log():
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        log_path = '../log/'
    else:
        log_path = '/var/log/zanhao/'
    fmt = '%(asctime)s - %(threadName)s - %(levelname)s - %(message)s'
    log = logging.getLogger('')
    fileTimeHandler = TimedRotatingFileHandler(log_path+'pdf_parse.log', "D", 1, 3)
    fileTimeHandler.suffix = "%Y%m%d"
    fileTimeHandler.setFormatter(logging.Formatter(fmt))
    logging.basicConfig(level=logging.DEBUG, format=fmt)
    log.addHandler(fileTimeHandler)


class pdf_parse():
    def __init__(self):
        self.threadpool = ThreadPool(256)

    def write_xls(self, pdf_list):
        book = xlwt.Workbook()
        sh = book.add_sheet('sheet1')
        for index, pdf in enumerate(pdf_list):
            sh.write(index, 0, pdf['stock_id'])
            sh.write(index, 1, pdf['stock_year'])
            sh.write(index, 2, pdf['judge_code'])
        book.save('xlsFile.xls')
        logging.info('write in success!')
        return None

    def main(self):
        path = '/Volumes/MobileHardDisk/annual_report/'
        pdf_list = []
        file_list_pdf = os.listdir(path)
        for file in file_list_pdf:
            if '.zip' in file:
                continue
            self.threadpool.add_task(self.balabala, path+file, pdf_list)
        self.threadpool.destroy()
        self.write_xls(pdf_list)

    def balabala(self, file, pdf_list):
        # pdf_list = []
        # for file in file_list_pdf:
        #     if '.zip' in file:
        #         continue
        pdf_dict = {}

        try:
            DATABASE_LOCK.acquire()
            hahaha = self.pdf_file(file)
            pdf_dict['judge_code'] = hahaha
            stock = file.split('.')[0].split('-')
            pdf_dict['stock_id'] = stock[0]
            pdf_dict['stock_year'] = stock[1]
            logging.info(json.dumps(pdf_dict))
            pdf_list.append(pdf_dict)
        except Exception as e:
            logging.info(e)
        finally:
            DATABASE_LOCK.release()

    def pdf_file(self, file):
        pdf_str = ''
        fp = open(file, 'rb')  # 以二进制读模式打开
        praser = PDFParser(fp)
        doc = PDFDocument()
        praser.set_document(doc)
        doc.set_parser(praser)
        doc.initialize()
        if not doc.is_extractable:
            return False
            # raise PDFTextExtractionNotAllowed
        else:
            rsrcmgr = PDFResourceManager()
            laparams = LAParams()
            device = PDFPageAggregator(rsrcmgr, laparams=laparams)
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            page_content = 0
            for page_num, page in enumerate(doc.get_pages()):
                page_num = page_num + 1
                if page_num == 40:
                    print(page_num)
                logging.info('now page: %s'%page_num)
                interpreter.process_page(page)

                layout = device.get_result()
                page_content = self.local_page(layout)
                if page_content == '3':
                    continue
                logging.info('check finished! closed pdf')
                fp.close()
                break
            return page_content

    def local_page(self, layout):
        a = []
        for x in layout:
            if (isinstance(x, LTTextBoxHorizontal)):
                a.append(x.get_text().replace('\n', ''))
        logging.info(str(a))

        for index, tt in enumerate(a):
            if '委托理财情况' in tt:
                if '√ 适用 □ 不适用' in a[index+1]:
                    return '1'
                elif '□ 适用 √ 不适用' in a[index+1]:
                    return '2'
        else:
            return '3'

    def parse(self):
        df = read_pdf('000038-2017.pdf', pages='40', multiple_tables=True)
        print(df[0].T, type(df[0].T))
        print(df[0]._get_values, type(df[0]._get_values))
        print(df[0]._obj_with_exclusions, type(df[0]._obj_with_exclusions))
        print(df[0]._selected_obj, type(df[0]._selected_obj))
        print(df[0]._values, type(df[0]._values))
        print(df[0].values, type(df[0].values))

        # for indexs in df:
        #     print(indexs)
        # convert_into(file_path+pdf_file, 'test.csv', encoding='utf-8', pages='all')


if __name__ == '__main__':
    config_log()
    asd = pdf_parse()
    asd.main()