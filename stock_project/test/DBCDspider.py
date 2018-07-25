# -*-coding: utf-8-*-
import hashlib
import logging
from logging.handlers import TimedRotatingFileHandler

import requests
from pyquery import PyQuery as pq
import torndb



def config_log():
    level = logging.INFO
    fmt = '%(asctime)s - %(threadName)s - %(levelname)s - %(message)s'
    log = logging.getLogger('')
    fileTimeHandler = TimedRotatingFileHandler('data_api.log', "D", 1, 3)
    fileTimeHandler.suffix = "%Y%m%d.log"
    fileTimeHandler.setFormatter(logging.Formatter(fmt))
    logging.basicConfig(level=level, format=fmt)
    log.addHandler(fileTimeHandler)


class DBCDspider():
    def __init__(self):
        self.session = requests.session()
        self.timeout = 10
        self.home_url = 'http://kjxy.dufe.edu.cn/'
        self.mysql_conn = torndb.Connection('47.91.237.174:3306', 'caishen', user='zanhao', password='zanhao_data_analysis')

    def search(self):
        try:
            response_home = self.session.get('http://kjxy.dufe.edu.cn/teacher/teacher.php?action=list&dstype=54', verify=False, timeout=self.timeout)
            b = pq(response_home.content)
            data_list = b('ul[id="teacher-list"] li')
            for data in data_list:
                new_url = self.home_url+b('li>a', data).attr('href')
                new_res = self.session.get(new_url, verify=False, timeout=self.timeout)
                b = pq(new_res.content)
                pages = b('div[id="pages_list"]>b:eq(1)').text().split('/')[-1]
                url = b('div[id="pages_list"]>a:first').attr('href')
                self.parse_detail(pages, url)
        except Exception as e:
            logging.info(e)

    def parse_detail(self, pages, url):
        judge = 1
        while True:
            new_url_list = url.split('&')
            for index, new in enumerate(new_url_list):
                if 'page=' in new:
                    new_url_list[index] = 'page=%s'%judge
            new_url = '&'.join(new_url_list)
            person_page = self.session.get(new_url, verify=False, timeout=self.timeout)
            b = pq(person_page.content)
            tr_list = b('div[id="padding"]>div[class="js-list"] tr')
            self.repackage(b, tr_list)
            judge = judge + 1
            if judge > int(pages):
                break

    def repackage(self, b, tr_list):
        for index, tr in enumerate(tr_list):
            if index == 0:
                continue
            member_dict = {}
            member_dict['name'] = b('tr>td:first', tr).text()
            member_dict['main_sub'] = b('tr>td:eq(1)', tr).text()
            member_dict['department'] = b('tr>td:eq(2)', tr).text()
            member_dict['email'] = b('tr>td:eq(3)', tr).text()
            detail_msg_url = self.home_url+b('tr>td:eq(4) a', tr).attr('href')
            res_dict = self.msg_detail(detail_msg_url)
            member_dict['member_detail'] = res_dict
            self.write_sql(member_dict)

    def write_sql(self, member_dict):
        sel_sql = "SELECT * FROM `member_list` WHERE `NAME`='%s' AND university='%s' AND email='%s';"%(member_dict['name'], u'东北财经大学会计学院', member_dict['email'])
        try:
            res = self.mysql_conn.query(sel_sql)
            if res == []:
                insert_sql = "INSERT INTO `member_list`(`NAME`, university, department, main_subject, phone_num, email) VALUES('%s','%s','%s','%s','%s','%s');"%(member_dict['name'], u'东北财经大学会计学院', member_dict['department'], member_dict['main_sub'], '', member_dict['email'])
                self.mysql_conn.execute(insert_sql)
                session = self.md5(member_dict['name']+u'东北财经大学会计学院'+member_dict['email'])
                sel_detail_sql = "SELECT * FROM `person_msg` WHERE SESSION='%s';"%(session)
                detail_res = self.mysql_conn.query(sel_detail_sql)
                if detail_res == []:
                    insert_detail_sql = "INSERT INTO `person_msg`(`SESSION`, `NAME`, sex, job_title, tutor_category, ethnicity, education, political_face, email, learning_experience, working_experience, research_results, honor) VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');"%(session, member_dict['name'], member_dict['member_detail']['sex'], member_dict['member_detail']['job_title'], member_dict['member_detail']['teacher_type'], member_dict['member_detail']['ethnicity'], member_dict['member_detail']['education'], member_dict['member_detail']['face'], member_dict['email'], member_dict['member_detail']['learning_experience'], member_dict['member_detail']['working_experience'], member_dict['member_detail']['research_result'], member_dict['member_detail']['honor'])
                    self.mysql_conn.execute(insert_detail_sql)
        except Exception as e:
            print e

    def msg_detail(self, detail_url):
        try:
            msg_detail_dict = {}
            res = self.session.get(detail_url, verify=False, timeout=self.timeout)
            b = pq(res.content)
            tr_list = b('div[id="padding"]>div[class="jsxx"]')
            msg_detail_dict['sex'] = b('tr:eq(1) td:first', tr_list).text()
            msg_detail_dict['job_title'] = b('tr:eq(1) td:eq(1)', tr_list).text()
            msg_detail_dict['teacher_type'] = b('tr:eq(2) td:first', tr_list).text()
            msg_detail_dict['ethnicity'] = b('tr:eq(3) td:first', tr_list).text()
            msg_detail_dict['education'] = b('tr:eq(4) td:first', tr_list).text()
            msg_detail_dict['face'] = b('tr:eq(4) td:eq(1)', tr_list).text()
            msg_detail_dict['email'] = b('tr:eq(5) td:eq(1)', tr_list).text()
            msg_detail_dict['learning_experience'] = b('tr:eq(7) td:eq(0)', tr_list).text()
            msg_detail_dict['working_experience'] = b('tr:eq(8) td:eq(0)', tr_list).text()
            msg_detail_dict['research_result'] = b('tr:eq(9) td:eq(0)', tr_list).text()
            msg_detail_dict['honor'] = b('tr:eq(10) td:eq(0)', tr_list).text()
            return msg_detail_dict
        except Exception as e:
            logging.info(e)
            return {}

    def md5(self, str):
        hl = hashlib.md5()
        hl.update(str.encode(encoding='utf-8'))
        return hl.hexdigest()


if __name__ == '__main__':
    config_log()
    res = DBCDspider()
    res.search()
