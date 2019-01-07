# -*-coding: utf-8-*-

# **************************file desc*****************************
import os
import subprocess
import sys
# from tabula.wrapper import read_pdf, convert_into
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBoxHorizontal
from pdfminer.pdfdocument import PDFDocument, PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfparser import PDFParser
from PyPDF2 import PdfFileReader
from tabula.wrapper import read_pdf

__author__ = 'arvin'
# createTime : 2019/1/2 14:24
# desc : this is new py file, please write your desc for this file
# ****************************************************************


class pdf_parse():
    def __init__(self):
        pass

    def pdf_file(self):
        pdf_str = ''
        fp = open('000038-2017.pdf', 'rb')  # 以二进制读模式打开
        praser = PDFParser(fp)
        doc = PDFDocument()
        praser.set_document(doc)
        doc.set_parser(praser)
        doc.initialize()
        if not doc.is_extractable:
            raise PDFTextExtractionNotAllowed
        else:
            rsrcmgr = PDFResourceManager()
            laparams = LAParams()
            device = PDFPageAggregator(rsrcmgr, laparams=laparams)
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            for page in doc.get_pages():
                # print(page)
                interpreter.process_page(page)
                layout = device.get_result()
                for x in layout:
                    if (isinstance(x, LTTextBoxHorizontal)):
                        if '委托理财' in x.get_text():
                            print(x.get_text())
                        # pdf_str = pdf_str + "%s\n" % x.get_text()
        # print(pdf_str)


        # file_list = os.listdir('F:/annual_report/')
        # for fil in file_list:
        #     if 'pdf' in fil or 'PDF' in fil:
        # self.parse('000038-2017.pdf')

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

    def asdasda(self):
        pdffilereader = PdfFileReader('000038-2017.pdf')
        doc_info = pdffilereader.getDocumentInfo()
        print('documentInfo = %s' % doc_info)

        pageLayout = pdffilereader.getPageLayout()
        print('pageLayout = %s ' % pageLayout)

        pageMode = pdffilereader.getPageMode()
        print('pageMode = %s' % pageMode)

        xmpMetadata = pdffilereader.getXmpMetadata()
        print('xmpMetadata  = %s ' % xmpMetadata)

        pageCount = pdffilereader.getNumPages()
        print('pageCount = %s' % pageCount)

        for index in range(0, pageCount):
            # 返回指定页编号的 pageObject
            pageObj = pdffilereader.getPage(index)
            print('index = %d , pageObj = %s' % (index, type(pageObj)))  # <class 'PyPDF2.pdf.PageObject'>
            # 获取 pageObject 在 PDF 文档中处于的页码
            pageNumber = pdffilereader.getPageNumber(pageObj)
            print('pageNumber = %s ' % pageNumber)



if __name__ == '__main__':
    asd = pdf_parse()
    asd.parse()