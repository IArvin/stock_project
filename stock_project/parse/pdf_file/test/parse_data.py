# -*-coding: utf-8-*-
import json
import logging
import os
from logging.handlers import TimedRotatingFileHandler
import xlwt
import sys
from xlutils.copy import copy
import xlrd
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter, PDFTextExtractionNotAllowed
from pdfminer.converter import TextConverter, PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBoxHorizontal
from pdfminer.pdfparser import PDFParser, PDFDocument
from io import StringIO
from io import open


# 数据归档

KEY_WORDS_DICT = {"资产类": "应收；存货；货币资金；递延所得税资产；投资性房地产；固定资产；在建工程；无形资产；预付；流动资产；金融资产；长期股权投资；生物性资产；",
                  "负债类": "应付；预收；递延所得税负债；短期借款；长期借款；其他应付款；应付银行承兑汇票；金融负债；应付职工薪酬；",
                  "收入类": "主营业务收入；其他业务收入；营业外收入；债务重组；政府补；投资收益；租赁；订单；拆迁补偿；",
                  "成本类": "成本；营业外支出；销售费用；管理费用；财务费用；利息；研发；广告；运输费用；所得税费用；水电费；三包损失；安全生产费；售后维护费；长期待摊费用；原材料采购；差旅费；",
                  "备抵科目类": "坏账准备；跌价准备；减值准备；未确认融资费用；商誉减值；",
                  "或有事项类": "诉讼；仲裁；或有负债；违约；冻结；预计负债；",
                  "公允价值类": "公允；金融工具；",
                  "信息披露类": "补充披露；详细介绍；详细说明；信息披露；公司未来发展的展望；披露义务；表外项目；缺少附注索引；",
                  "内部控制类": "内部控制；内控；实际控制人；会计差错更正；财务报表重述；舞弊；",
                  "业绩奖励类": "净资产收益率；净利润；净利润；净利率；股票期权；毛利率；亏损；激励；持股计划；分红；绩效；关键管理人员薪酬；",
                  "行业及经营类": "项目进展；主要子公司、参股公司分析；同行业；周转率；孙公司；竞争对手；经营模式；竞争优劣势；行业许可；行业资质；行业地位；季节波动；同业竞争；协同效应；上游；中游；下游；",
                  "公司治理结构类": "独立董事；离职；辞职；董事；监事；高管；审计委员会；股东大会；控制权；高管变动；换届；实际控制人；",
                  "非关联股权变更": "资产出售；股权转让；重大资产重组；重大资产出售；股份出售；股权回购；业绩补偿；重组业绩承诺；业绩对赌；大股东减持；",
                  "关联交易类": "其他应收款；关联交易；担保；股权质押；资金拆借；占用上市公司资金；关联方；经营性占用；控股股东；输送；",
                  "会计政策类": "会计差错；会计政策变更；追溯调整；企业会计准则；会计估计变更；会计处理；跨期确认收入；跨期转结成本；套期会计；挂账；追溯重述；合并范围；",
                  "现金流量类": "现金流；现金净流量；收到的现金；收回的现金；资金往来",
                  "审计类": "非标准意见；发表专项意见；发表明确意见；非标准审计意见；年审会计师；会计师事务所；审计报告；发表核查意见；审计证据；审计程序；会计师发表意见；审计机构；",
                  "客户供应商类": "客户；供应商；",
                  "税类": "税；",
                  "风险类": "退市风险警示；汇率风险；投资风险；偿债能力；经营风险；公司债到期兑付；担保；票据结算风险；流动性风险；应收账款回收风险；抵押；质押；",
                  "其他类": "募集资金；委托理财；理财产品；保理；专利；生产技术；污染；环保；保荐机构核查；债务重组；非经常性损益；"}
test = ["内部控制类", "税类", "或有事项类", "现金流量类", "业绩奖励类", "其他类", "审计类", "公允价值类", "资产类", "收入类", "负债类", "成本类", "信息披露类", "备抵科目类",
        "行业及经营类", "关联交易类", "会计政策类", "公司治理结构类", "客户供应商类", "非关联股权变更", "风险类"]
segment_key = {"Internal_Control": "内部控制类", "taxCategory": "税类", "OrContingentClass": "或有事项类", "CashFlowClass": "现金流量类",
               "PerformanceAwards": "业绩奖励类", "other": "其他类", "AuditClass": "审计类", "FairValueClass": "公允价值类",
               "AssetClass": "资产类", "RevenueCategory": "收入类", "Liability": "负债类", "CostClass": "成本类",
               "InformationDisclosures": "信息披露类", "AllowableAccountClass": "备抵科目类",
               "IndustryAndBusinessCategory": "行业及经营类", "AssociateTransactions": "关联交易类", "AccountingPolicies": "会计政策类",
               "CorporateGovernanceStructure": "公司治理结构类", "CustomerSupplierCategory": "客户供应商类",
               "ChangeOfNonRelatedEquity": "非关联股权变更", "RiskClass": "风险类"}

def config_log():
    fmt = '%(asctime)s - %(threadName)s - %(levelname)s - %(message)s'
    log = logging.getLogger('')
    fileTimeHandler = TimedRotatingFileHandler('../../../log/parse_data.log', "D", 1, 3)
    fileTimeHandler.suffix = "%Y%m%d"
    fileTimeHandler.setFormatter(logging.Formatter(fmt))
    logging.basicConfig(level=logging.DEBUG, format=fmt)
    log.addHandler(fileTimeHandler)


class Data_archiving(object):
    def __init__(self):
        pass

    def getfiles(self):
        pdf_file_list = []
        for file in os.listdir('/Users/arvin/Documents/huning/stock_project/stock_project/parse/pdf_file/test/pdf_file/car-database'):
            if '.pdf' in file or '.PDF' in file:
                pdf_file_list.append('/Users/arvin/Documents/huning/stock_project/stock_project/parse/pdf_file/test/pdf_file/car-database/'+file)
            if '.doc' in file or '.DOC' in file or '.docx' in file or '.DOCX' in file:
                print(file)
        return pdf_file_list

    def readPDF(self):
        pdf_file_list = self.getfiles()
        # pdf_file_list = ['000007-2016-1.pdf']
        for pdf_file in pdf_file_list:
            pdf_str = ''
            fp = open(pdf_file, 'rb')  # 以二进制读模式打开
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
                print(pdf_file)
                for page in doc.get_pages():
                    print(page)
                    interpreter.process_page(page)
                    layout = device.get_result()
                    for x in layout:
                        if (isinstance(x, LTTextBoxHorizontal)):
                            pdf_str = pdf_str + "%s\n" % x.get_text()
            size = os.path.getsize(pdf_file)
            pdf_size = str(float(format(size / 1024))) + 'KB'
            segment = self.archiving(pdf_str)
            print(json.dumps(segment))
            self.update_xls(pdf_file, pdf_size, segment)

            # pdf_str = ''
            # uipath = unicode(pdf_file, "utf8")
            # fp = open(uipath, 'r', encoding='utf-8')
            # parser_pdf = PDFParser(fp)
            # doc = PDFDocument(parser_pdf)
            # parser_pdf.set_document(doc)
            # resource = PDFResourceManager()
            # laparam = LAParams()
            # device = PDFPageAggregator(resource, laparams=laparam)
            # interpreter = PDFPageInterpreter(resource, device)
            # for page in PDFPage.create_pages(doc):
            #     interpreter.process_page(page)
            #     layout = device.get_result()
            #     for out in layout:
            #         if hasattr(out, 'get_text'):
            #             if out.get_text() == ' \n':
            #                 continue
            #             pdf_str = pdf_str + "%s" % out.get_text()
            # print(pdf_str)
            # print(type(pdf_str))
            # size = os.path.getsize(pdf_file)
            # pdf_size = str(float(format(size / 1024))) + 'KB'
            # segment = self.archiving(pdf_str)
            # self.update_xls(pdf_file, pdf_size, segment)

    def archiving(self, pdf_str):
        segment = {}
        # 关键词  “流动资产”、“固定资产”、“无形资产”（对应资产类赋值为1）、“资产减值准备”（对应备抵类赋值为1）、“会计处理”（对应会计政策类赋值为1）、“披露义务”（对应信息披露类赋值为1）。

        key_list = KEY_WORDS_DICT.keys()

        for key in key_list:
            for word in KEY_WORDS_DICT[key].split('；'):
                if word in pdf_str:
                    for seg in segment_key.keys():
                        print(segment_key[seg], type(segment_key[seg]), key, type(key))
                        if segment_key[seg] == key:
                            segment[seg] = "1"
                            break
                    break
            else:
                for seg in segment_key.keys():
                    if segment_key[seg] == key:
                        segment[seg] = "0"
                        break
        return segment

    def update_xls(self, pdf_file, pdf_size, segment):
        search_list = self.read_xls()
        oldWb = xlrd.open_workbook('xlsFile.xls', formatting_info=True)
        newWb = copy(oldWb)
        for index, search in enumerate(search_list):
            if index <= 1:
                continue
            if str(search['stkcd']) != pdf_file.split('/')[-1].split('-')[0]:
                continue

            if '半' in pdf_file.split('/')[-1].split('-')[1] or ' ' in pdf_file.split('/')[-1].split('-')[1] or '内控' in pdf_file.split('/')[-1].split('-')[1] or 'B' in pdf_file.split('/')[-1].split('-')[1] or '季' in pdf_file.split('/')[-1].split('-')[1] or '?' in pdf_file.split('/')[-1].split('-')[1]:
                if str(int(str(search['year']).replace('.0', ''))) != pdf_file.split('/')[-1].split('-')[1][0:4]:
                    continue
            else:
                if str(int(str(search['year']).replace('.0', ''))) != pdf_file.split('/')[-1].split('-')[1]:
                    continue

            print(newWb)
            print(int(search['rows']))
            newWs = newWb.get_sheet(0)
            newWs.write(int(search['rows']), 6, pdf_size)
            newWs.write(int(search['rows']), 16, segment['AssetClass'])
            newWs.write(int(search['rows']), 17, segment['Liability'])
            newWs.write(int(search['rows']), 18, segment['RevenueCategory'])
            newWs.write(int(search['rows']), 19, segment['CostClass'])

            newWs.write(int(search['rows']), 20, segment['AllowableAccountClass'])
            newWs.write(int(search['rows']), 21, segment['OrContingentClass'])
            newWs.write(int(search['rows']), 22, segment['FairValueClass'])
            newWs.write(int(search['rows']), 23, segment['InformationDisclosures'])
            newWs.write(int(search['rows']), 24, segment['Internal_Control'])
            newWs.write(int(search['rows']), 25, segment['PerformanceAwards'])
            newWs.write(int(search['rows']), 26, segment['IndustryAndBusinessCategory'])
            newWs.write(int(search['rows']), 27, segment['CorporateGovernanceStructure'])
            newWs.write(int(search['rows']), 28, segment['ChangeOfNonRelatedEquity'])
            newWs.write(int(search['rows']), 29, segment['AssociateTransactions'])
            newWs.write(int(search['rows']), 30, segment['AccountingPolicies'])
            newWs.write(int(search['rows']), 31, segment['CashFlowClass'])
            newWs.write(int(search['rows']), 32, segment['AuditClass'])
            newWs.write(int(search['rows']), 33, segment['CustomerSupplierCategory'])
            newWs.write(int(search['rows']), 34, segment['taxCategory'])
            newWs.write(int(search['rows']), 35, segment['RiskClass'])
            newWs.write(int(search['rows']), 36, segment['other'])
            print("write new values ok")
            break
        newWb.save("xlsFile.xls")
        print("save with same name ok")

    def write_xls(self):
        search_list = self.read_xls()
        book = xlwt.Workbook()
        sh = book.add_sheet('sheet1')
        for search in search_list:
            sh.write(int(search['rows']), 0, search['stkcd'])
            sh.write(int(search['rows']), 1, search['exchange'])  # 交易所
            sh.write(int(search['rows']), 2, search['year'])
            sh.write(int(search['rows']), 3, search['timeperio'])
            sh.write(int(search['rows']), 4, search['CL'])
            sh.write(int(search['rows']), 5, search['semi-year'])
            sh.write(int(search['rows']), 6, search['pdf1'])
            sh.write(int(search['rows']), 7, search['pdf2'])
            sh.write(int(search['rows']), 8, search['number'])
            sh.write(int(search['rows']), 9, search['date'])
            sh.write(int(search['rows']), 10, search['date0'])
            sh.write(int(search['rows']), 11, search['date2'])

            sh.write(int(search['rows']), 12, search['auditor'])
            sh.write(int(search['rows']), 13, search['times'])
            sh.write(int(search['rows']), 14, search['delay'])
            sh.write(int(search['rows']), 15, search['note'])

            sh.write(int(search['rows']), 16, search['class1'])
            sh.write(int(search['rows']), 17, search['class2'])
            sh.write(int(search['rows']), 18, search['class3'])
            sh.write(int(search['rows']), 19, search['class4'])
            sh.write(int(search['rows']), 20, search['class5'])
            sh.write(int(search['rows']), 21, search['class6'])
            sh.write(int(search['rows']), 22, search['class7'])
            sh.write(int(search['rows']), 23, search['class8'])
            sh.write(int(search['rows']), 24, search['class9'])
            sh.write(int(search['rows']), 25, search['class10'])
            sh.write(int(search['rows']), 26, search['class11'])
            sh.write(int(search['rows']), 27, search['class12'])
            sh.write(int(search['rows']), 28, search['class13'])
            sh.write(int(search['rows']), 29, search['class14'])
            sh.write(int(search['rows']), 30, search['class15'])
            sh.write(int(search['rows']), 31, search['class16'])
            sh.write(int(search['rows']), 32, search['class17'])
            sh.write(int(search['rows']), 33, search['class18'])
            sh.write(int(search['rows']), 34, search['class19'])
            sh.write(int(search['rows']), 35, search['class20'])
            sh.write(int(search['rows']), 36, search['class21'])
        book.save('xlsFile.xls')
        logging.info('write in success!')

    def read_xls(self):
        book = xlrd.open_workbook('CL_CAR.xlsx')
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
                data_dict['semi-year'] = sheet.cell(nrow, 5).value
                data_dict['pdf1'] = sheet.cell(nrow, 6).value
                data_dict['pdf2'] = sheet.cell(nrow, 7).value
                data_dict['number'] = sheet.cell(nrow, 8).value
                data_dict['date'] = sheet.cell(nrow, 9).value
                data_dict['date0'] = sheet.cell(nrow, 10).value
                data_dict['date2'] = sheet.cell(nrow, 11).value
                data_dict['auditor'] = sheet.cell(nrow, 12).value
                data_dict['times'] = sheet.cell(nrow, 13).value
                data_dict['delay'] = sheet.cell(nrow, 14).value
                data_dict['note'] = sheet.cell(nrow, 15).value

                data_dict['class1'] = sheet.cell(nrow, 16).value
                data_dict['class2'] = sheet.cell(nrow, 17).value
                data_dict['class3'] = sheet.cell(nrow, 18).value
                data_dict['class4'] = sheet.cell(nrow, 19).value
                data_dict['class5'] = sheet.cell(nrow, 20).value
                data_dict['class6'] = sheet.cell(nrow, 21).value
                data_dict['class7'] = sheet.cell(nrow, 22).value
                data_dict['class8'] = sheet.cell(nrow, 23).value
                data_dict['class9'] = sheet.cell(nrow, 24).value
                data_dict['class10'] = sheet.cell(nrow, 25).value
                data_dict['class11'] = sheet.cell(nrow, 26).value
                data_dict['class12'] = sheet.cell(nrow, 27).value
                data_dict['class13'] = sheet.cell(nrow, 28).value
                data_dict['class14'] = sheet.cell(nrow, 29).value
                data_dict['class15'] = sheet.cell(nrow, 30).value
                data_dict['class16'] = sheet.cell(nrow, 31).value
                data_dict['class17'] = sheet.cell(nrow, 32).value
                data_dict['class18'] = sheet.cell(nrow, 33).value
                data_dict['class19'] = sheet.cell(nrow, 34).value
                data_dict['class20'] = sheet.cell(nrow, 35).value
                data_dict['class21'] = sheet.cell(nrow, 36).value

                data_dict['rows'] = nrow
            else:
                data_dict['stkcd'] = sheet.cell(nrow, 0).value
                data_dict['exchange'] = sheet.cell(nrow, 1).value
                data_dict['year'] = sheet.cell(nrow, 2).value
                data_dict['timeperio'] = sheet.cell(nrow, 3).value
                data_dict['CL'] = sheet.cell(nrow, 4).value
                data_dict['semi-year'] = sheet.cell(nrow, 5).value
                data_dict['pdf1'] = sheet.cell(nrow, 6).value
                data_dict['pdf2'] = sheet.cell(nrow, 7).value
                data_dict['number'] = sheet.cell(nrow, 8).value
                data_dict['date'] = sheet.cell(nrow, 9).value
                data_dict['date0'] = sheet.cell(nrow, 10).value
                data_dict['date2'] = sheet.cell(nrow, 11).value
                data_dict['auditor'] = sheet.cell(nrow, 12).value
                data_dict['times'] = sheet.cell(nrow, 13).value
                data_dict['delay'] = sheet.cell(nrow, 14).value
                data_dict['note'] = sheet.cell(nrow, 15).value

                data_dict['class1'] = sheet.cell(nrow, 16).value
                data_dict['class2'] = sheet.cell(nrow, 17).value
                data_dict['class3'] = sheet.cell(nrow, 18).value
                data_dict['class4'] = sheet.cell(nrow, 19).value
                data_dict['class5'] = sheet.cell(nrow, 20).value
                data_dict['class6'] = sheet.cell(nrow, 21).value
                data_dict['class7'] = sheet.cell(nrow, 22).value
                data_dict['class8'] = sheet.cell(nrow, 23).value
                data_dict['class9'] = sheet.cell(nrow, 24).value
                data_dict['class10'] = sheet.cell(nrow, 25).value
                data_dict['class11'] = sheet.cell(nrow, 26).value
                data_dict['class12'] = sheet.cell(nrow, 27).value
                data_dict['class13'] = sheet.cell(nrow, 28).value
                data_dict['class14'] = sheet.cell(nrow, 29).value
                data_dict['class15'] = sheet.cell(nrow, 30).value
                data_dict['class16'] = sheet.cell(nrow, 31).value
                data_dict['class17'] = sheet.cell(nrow, 32).value
                data_dict['class18'] = sheet.cell(nrow, 33).value
                data_dict['class19'] = sheet.cell(nrow, 34).value
                data_dict['class20'] = sheet.cell(nrow, 35).value
                data_dict['class21'] = sheet.cell(nrow, 36).value
                data_dict['rows'] = nrow
            data_list.append(data_dict)
        return data_list


if __name__ == '__main__':
    config_log()
    res = Data_archiving()
    res.write_xls()
    res.readPDF()
