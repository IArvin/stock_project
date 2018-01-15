# -*-coding: utf-8-*-
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter, PDFPageAggregator
from pdfminer.layout import LAParams
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from io import StringIO
from io import open




def readPDF(pdf_file):
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
        print layout
        for out in layout:
            if hasattr(out, 'get_text'):
                print out.get_text()
    return None


if __name__ == '__main__':
    pdf_file = '002006_2017-09-26.PDF'
    readPDF(pdf_file)