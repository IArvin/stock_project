# -*-coding: utf-8-*-
import logging
import os

import xlwt
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from xlutils.copy import copy
import xlrd
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter, PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBoxHorizontal
from pdfminer.pdfparser import PDFParser
from io import StringIO
from io import open


# 数据归档

class Data_archiving(object):
    def __init__(self):
        pass

    def getfiles(self):
        pdf_file_list = []
        for file in os.listdir('/Users/arvin/Documents/huning/stock_project/stock_project/parse/pdf_file/test'):
            if '.pdf' in file or '.PDF' in file:
                pdf_file_list.append(file)
        return pdf_file_list

    def readPDF(self):
        pdf_file_list = self.getfiles()
        # pdf_file_list = ['000007-2016-1.pdf']
        for pdf_file in pdf_file_list:
            # pdf_str = ''
            # fp = open(pdf_file, 'rb')  # 以二进制读模式打开
            # praser = PDFParser(fp)
            # doc = PDFDocument()
            # praser.set_document(doc)
            # doc.set_parser(praser)
            # doc.initialize()
            # if not doc.is_extractable:
            #     raise PDFTextExtractionNotAllowed
            # else:
            #     rsrcmgr = PDFResourceManager()
            #     laparams = LAParams()
            #     device = PDFPageAggregator(rsrcmgr, laparams=laparams)
            #     interpreter = PDFPageInterpreter(rsrcmgr, device)
            #
            #     for page in doc.get_pages():
            #         interpreter.process_page(page)
            #         layout = device.get_result()
            #         for x in layout:
            #             if (isinstance(x, LTTextBoxHorizontal)):
            #                 pdf_str = pdf_str + "%s\n" % x.get_text()
            # size = os.path.getsize(pdf_file)
            # pdf_size = str(float(format(size / 1024))) + 'KB'
            # segment = self.archiving(pdf_str)
            # self.update_xls(pdf_file, pdf_size, segment)

            pdf_str = ''
            fp = open(pdf_file, 'rb')
            parser_pdf = PDFParser(fp)
            doc = PDFDocument(parser_pdf)
            parser_pdf.set_document(doc)
            resource = PDFResourceManager()
            laparam = LAParams()
            device = PDFPageAggregator(resource, laparams=laparam)
            interpreter = PDFPageInterpreter(resource, device)
            for page in PDFPage.create_pages(doc):
                interpreter.process_page(page)
                layout = device.get_result()
                for out in layout:
                    if hasattr(out, 'get_text'):
                        if out.get_text() == ' \n':
                            continue
                        pdf_str = pdf_str + "%s\n" % out.get_text()
            size = os.path.getsize(pdf_file)
            pdf_size = str(float(format(size/1024)))+'KB'
            segment = self.archiving(pdf_str)
            self.update_xls(pdf_file, pdf_size, segment)

    def archiving(self, pdf_str):
        segment = {}
        # 关键词  “流动资产”、“固定资产”、“无形资产”（对应资产类赋值为1）、“资产减值准备”（对应备抵类赋值为1）、“会计处理”（对应会计政策类赋值为1）、“披露义务”（对应信息披露类赋值为1）。
        if (u'流动资产' in pdf_str) or (u'固定资产' in pdf_str) or (u'无形资产' in pdf_str):
            segment['Asset_class'] = '1'
        else:
            segment['Asset_class'] = '0'

        if (u'资产减值准备' in pdf_str):
            segment['Assortment'] = '1'
        else:
            segment['Assortment'] = '0'

        if (u'会计处理' in pdf_str):
            segment['Accounting_policy'] = '1'
        else:
            segment['Accounting_policy'] = '0'

        if u'披露义务' in pdf_str:
            segment['Disclosure'] = '1'
        else:
            segment['Disclosure'] = '0'
        return segment

    def update_xls(self, pdf_file, pdf_size, segment):
        search_list = self.read_xls()
        oldWb = xlrd.open_workbook('xlsFile.xls', formatting_info=True)
        newWb = copy(oldWb)
        for index, search in enumerate(search_list):
            if index <= 1:
                continue
            if str(search['stkcd']) != pdf_file.split('-')[0]:
                continue
            if str(int(str(search['year']).replace('.0', ''))) != pdf_file.split('-')[1]:
                continue
            print(newWb)
            print(int(search['rows']))
            newWs = newWb.get_sheet(0)
            newWs.write(int(search['rows']), 5, pdf_size)
            newWs.write(int(search['rows']), 11, segment['Asset_class'])
            newWs.write(int(search['rows']), 15, segment['Assortment'])
            newWs.write(int(search['rows']), 25, segment['Accounting_policy'])
            newWs.write(int(search['rows']), 18, segment['Disclosure'])
            print("write new values ok")
        newWb.save("xlsFile.xls")
        print("save with same name ok")

    def write_xls(self, pdf_file, pdf_size, segment):
        search_list = self.read_xls()
        book = xlwt.Workbook()
        sh = book.add_sheet('sheet1')
        for search in search_list:
            sh.write(int(search['rows']), 0, search['stkcd'])
            sh.write(int(search['rows']), 1, search['exchange'])   # 交易所
            sh.write(int(search['rows']), 2, search['year'])
            sh.write(int(search['rows']), 3, search['timeperio'])
            sh.write(int(search['rows']), 4, search['CL'])
            sh.write(int(search['rows']), 5, search['pdf1'])
            sh.write(int(search['rows']), 6, search['pdf2'])
            sh.write(int(search['rows']), 7, search['number'])
            sh.write(int(search['rows']), 8, search['date'])
            sh.write(int(search['rows']), 9, search['date0'])
            sh.write(int(search['rows']), 10, search['date2'])
            sh.write(int(search['rows']), 11, search['class1'] )
            sh.write(int(search['rows']), 12, search['class2'] )
            sh.write(int(search['rows']), 13, search['class3'] )
            sh.write(int(search['rows']), 14, search['class4'] )
            sh.write(int(search['rows']), 15, search['class5'] )
            sh.write(int(search['rows']), 16, search['class6'] )
            sh.write(int(search['rows']), 17, search['class7'] )
            sh.write(int(search['rows']), 18, search['class8'] )
            sh.write(int(search['rows']), 19, search['class9'] )
            sh.write(int(search['rows']), 20, search['class10'])
            sh.write(int(search['rows']), 21, search['class11'])
            sh.write(int(search['rows']), 22, search['class12'])
            sh.write(int(search['rows']), 23, search['class13'])
            sh.write(int(search['rows']), 24, search['class14'])
            sh.write(int(search['rows']), 25, search['class15'])
            sh.write(int(search['rows']), 26, search['class16'])
            sh.write(int(search['rows']), 27, search['class17'])
            sh.write(int(search['rows']), 28, search['class18'])
            sh.write(int(search['rows']), 29, search['class19'])
            sh.write(int(search['rows']), 30, search['class20'])
            sh.write(int(search['rows']), 31, search['class21'])
        book.save('xlsFile.xls')
        logging.info('write in success!')

    def read_xls(self):
        book = xlrd.open_workbook('demo.xls')
        sheet = book.sheets()[0]
        nrows = sheet.nrows

        data_list = []
        for nrow in range(0, nrows):
            data_dict = {}
            if nrow > 1:
                data_dict['stkcd'] = sheet.cell(nrow, 0).value
                data_dict['exchange'] = sheet.cell(nrow, 1).value
                data_dict['year'] = sheet.cell(nrow, 2).value
                data_dict['timeperio'] = sheet.cell(nrow, 3).value
                data_dict['CL'] = sheet.cell(nrow, 4).value
                data_dict['pdf1'] = sheet.cell(nrow, 5).value
                data_dict['pdf2'] = sheet.cell(nrow, 6).value
                data_dict['number'] = sheet.cell(nrow, 7).value
                data_dict['date'] = sheet.cell(nrow, 8).value
                data_dict['date0'] = sheet.cell(nrow, 9).value
                data_dict['date2'] = sheet.cell(nrow, 10).value

                data_dict['class1'] = sheet.cell(nrow, 11).value
                data_dict['class2'] = sheet.cell(nrow, 12).value
                data_dict['class3'] = sheet.cell(nrow, 13).value
                data_dict['class4'] = sheet.cell(nrow, 14).value
                data_dict['class5'] = sheet.cell(nrow, 15).value
                data_dict['class6'] = sheet.cell(nrow, 16).value
                data_dict['class7'] = sheet.cell(nrow, 17).value
                data_dict['class8'] = sheet.cell(nrow, 18).value
                data_dict['class9'] = sheet.cell(nrow, 19).value
                data_dict['class10'] = sheet.cell(nrow, 20).value
                data_dict['class11'] = sheet.cell(nrow, 21).value
                data_dict['class12'] = sheet.cell(nrow, 22).value
                data_dict['class13'] = sheet.cell(nrow, 23).value
                data_dict['class14'] = sheet.cell(nrow, 24).value
                data_dict['class15'] = sheet.cell(nrow, 25).value
                data_dict['class16'] = sheet.cell(nrow, 26).value
                data_dict['class17'] = sheet.cell(nrow, 27).value
                data_dict['class18'] = sheet.cell(nrow, 28).value
                data_dict['class19'] = sheet.cell(nrow, 29).value
                data_dict['class20'] = sheet.cell(nrow, 30).value
                data_dict['class21'] = sheet.cell(nrow, 31).value

                data_dict['rows'] = nrow
            else:
                data_dict['stkcd'] = sheet.cell(nrow, 0).value
                data_dict['exchange'] = sheet.cell(nrow, 1).value
                data_dict['year'] = sheet.cell(nrow, 2).value
                data_dict['timeperio'] = sheet.cell(nrow, 3).value
                data_dict['CL'] = sheet.cell(nrow, 4).value
                data_dict['pdf1'] = sheet.cell(nrow, 5).value
                data_dict['pdf2'] = sheet.cell(nrow, 6).value
                data_dict['number'] = sheet.cell(nrow, 7).value
                data_dict['date'] = sheet.cell(nrow, 8).value
                data_dict['date0'] = sheet.cell(nrow, 9).value
                data_dict['date2'] = sheet.cell(nrow, 10).value

                data_dict['class1'] = sheet.cell(nrow, 11).value
                data_dict['class2'] = sheet.cell(nrow, 12).value
                data_dict['class3'] = sheet.cell(nrow, 13).value
                data_dict['class4'] = sheet.cell(nrow, 14).value
                data_dict['class5'] = sheet.cell(nrow, 15).value
                data_dict['class6'] = sheet.cell(nrow, 16).value
                data_dict['class7'] = sheet.cell(nrow, 17).value
                data_dict['class8'] = sheet.cell(nrow, 18).value
                data_dict['class9'] = sheet.cell(nrow, 19).value
                data_dict['class10'] = sheet.cell(nrow, 20).value
                data_dict['class11'] = sheet.cell(nrow, 21).value
                data_dict['class12'] = sheet.cell(nrow, 22).value
                data_dict['class13'] = sheet.cell(nrow, 23).value
                data_dict['class14'] = sheet.cell(nrow, 24).value
                data_dict['class15'] = sheet.cell(nrow, 25).value
                data_dict['class16'] = sheet.cell(nrow, 26).value
                data_dict['class17'] = sheet.cell(nrow, 27).value
                data_dict['class18'] = sheet.cell(nrow, 28).value
                data_dict['class19'] = sheet.cell(nrow, 29).value
                data_dict['class20'] = sheet.cell(nrow, 30).value
                data_dict['class21'] = sheet.cell(nrow, 31).value
                data_dict['rows'] = nrow
            data_list.append(data_dict)
        return data_list


if __name__ == '__main__':
    res = Data_archiving()
    res.readPDF()