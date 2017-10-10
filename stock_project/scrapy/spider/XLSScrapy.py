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


# createTime: 2017-10-09 16:02:05
# desc: EXCEL表单中问询公告相关数据下载


class XLSScrapy(scrapy):
    def __init__(self):
        super(XLSScrapy, self).__init__()
        self.session = requests.session()
        self.timeout = 15

    def read_excel(self):
        import xlrd
        mainData_book = xlrd.open_workbook("../../tools/inquiry_announcement.xls", formatting_info=True)
        mainData_sheet = mainData_book.sheet_by_index(0)
        print mainData_sheet
        for row in range(1, 101):
            rowValues = mainData_sheet.row_values(row, start_colx=0, end_colx=8)
            print rowValues

            link = mainData_sheet.hyperlink_map.get((row, 1))
            url = '(No URL)' if link is None else link.url_or_path
            print link
            print url

        # book = xlrd.open_workbook('../../tools/inquiry_announcement.xls',  formatting_info=True)
        # sheet = book.sheets()[0]
        # nrows = sheet.nrows
        # for nrow in xrange(1, nrows):
        #     announcement_time = sheet.cell(nrow, 0).value
        #     stock_id = sheet.cell(nrow, 1).value
        #     url = sheet.cell(nrow, 2)
        #     url = sheet
        #     print announcement_time, stock_id, url

    def main(self):
        self.read_excel()
        return None


if __name__ == '__main__':
    res = XLSScrapy()
    res.main()