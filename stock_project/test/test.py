# -*-coding: utf-8-*-
import hashlib
import xlrd
import logging
import torndb


class op():
    def __init__(self):
        self.conn = torndb.Connection('47.91.237.174:3306', database='caishen', user='zanhao', password='zanhao_data_analysis')
        self.filter_email = 'kevin_linkai<kevin_linkai@163.com>,   574177931<574177931@qq.com>,   wpoven<wpoven@163.com>,   405734149<405734149@qq.com>,   438835131<438835131@qq.com>,   455790869<455790869@qq.com>,   956569872<956569872@qq.com>, lightwinyu<lightwinyu@126.com>,   yuzhi_2014<yuzhi_2014@163.com>,   757602378<757602378@qq.com>,   Zhang_chao_010<Zhang_chao_010@163.com>,   14210690050<14210690050@fudan.edu.cn>,   277687436<277687436@163.com>,   1728047049<1728047049@qq.com>,   ZJKstalin<ZJKstalin@163.com>,   zhjingxin<zhjingxin@gzhu.edu.cn>,   junxiazhang0909<junxiazhang0909@qq.com>,   l.zhang<l.zhang@nau.edu.cn>,   minzhang07<minzhang07@126.com>,   zmxing1619<zmxing1619@126.com>,   zhangrong19930928<zhangrong19930928@126.com>,   zhang1101ting<zhang1101ting@126.com>,   zhangwei71622<zhangwei71622@163.com>,   zhangweiqian<zhangweiqian@suibe.edu.cn>,   tjcjzx209<tjcjzx209@163.com>,   384666980<384666980@qq.com>,   164207950<164207950@qq.com>,   390245113<390245113@qq.com>,   1531145701<1531145701@qq.com>,   zhangzhang0427<zhangzhang0427@ruc.edu.cn>,   18710995710<18710995710@163.com>,   1271656091<1271656091@qq.com>,   352006840<352006840@qq.com>,   zhwh<zhwh@sicnu.end.cn>,   zm6040<zm6040@aliyun.com>,   celinnazhn<celinnazhn@163.com>,   zhouq95<zhouq95@mail2.sysu.edu.cn>,   zhouwei23456<zhouwei23456@126.com>,   shanshanzhu707<shanshanzhu707@163.com>,   1297761063<1297761063@qq.com>,   zhuzhaozhen2009<zhuzhaozhen2009@163.com>,   975072580<975072580@qq.com>, wwj625<wwj625@163.com>,   765242895<765242895@qq.com>,   tjutwxj2015<tjutwxj2015@163.com>,   beanwangxueding<beanwangxueding@outlook.com>,   wangyy0801<wangyy0801@163.com>,   wangyi_emily<wangyi_emily@126.com>,   sufewangzw<sufewangzw@yeah.net>,   zhxlwtg<zhxlwtg@163.com>,   riguangwen<riguangwen@126.com>,   wxi1995<wxi1995@qq.com>,   wry99<wry99@163.com>,   cquemilywu<cquemilywu@126.com>,   pjwuxia<pjwuxia@163.com>,   1720660031<1720660031@qq.com>,   515106423<515106423@qq.com>,   921226855<921226855@qq.com>,   xiaoliang7<xiaoliang7@hnu.edu.cn>,   hfiyue<hfiyue@126.com>,   xie_mingzhi<xie_mingzhi@qq.com>,   xionglingyun1988<xionglingyun1988@126.com>,   563638312<563638312@qq.com>,   floraxcy666<floraxcy666@163.com>,   xfahnu<xfahnu@qq.com>,   xusi<xusi@m.scnu.edu.cn>,   xusi0216<xusi0216@163.com>,   1245095071<1245095071@qq.com>,   xuxingmei<xuxingmei@ruc.edu.cn>,   1258503433<1258503433@qq.com>,   daishuxyp<daishuxyp@163.com>,   B.Xue<B.Xue@soton.ac.uk>,   2516532762<2516532762@qq.com>,   yanwch3.14<yanwch3.14@sem.tsinghua.edu.cn>,   392966414<392966414@qq.com>,   spondee1980<spondee1980@163.com>,   yangchao<yangchao@email.cufe.edu.cn>,   124354600<124354600@qq.com>,   victory823<victory823@163.com>,   1157749768<1157749768@qq.com>,   yangyulong_accounting<yangyulong_accounting@aliyun.com>,   543375204<543375204@qq.com>,   yinjingwei2008<yinjingwei2008@163.com>,   yqhua123<yqhua123@163.com>,   1271358275<1271358275@qq.com>,   tufe9826<tufe9826@163.com>,   15110690034<15110690034@fudan.edu.cn>,   yuhaoyang1105<yuhaoyang1105@163.com>,   yujq.12<yujq.12@sem.tsinghua.edu.cn>,   bubbleyusu<bubbleyusu@126.com>, yingliu0329<yingliu0329@outlook.com>,   lougil<lougil@126.com>,   ludi<ludi@snnu.edu.cn>,   y_yaofei33<y_yaofei33@163.com>,   yg-luo<yg-luo@foxmail.com>,   510953381<510953381@qq.com>,   researchlkf<researchlkf@126.com>,   maruibox<maruibox@163.com>,   matao_work<matao_work@126.com>,   maying_tracy<maying_tracy@163.com>,   mazhiying999<mazhiying999@126.com>,   18711170136<18711170136@163.com>,   mx13838071226<mx13838071226@163.com>,   niezi_zuel<niezi_zuel@foxmail.com>,   13116039830<13116039830@163.com>,   panjianping11<panjianping11@126.com>,   gdkjxph<gdkjxph@gzhu.edu.cn>,   15113185<15113185@bjtu.edu.cn>,   474911826<474911826@qq.com>,   qhx0555<qhx0555@163.com>,   blairqin.xjtu+conf<blairqin.xjtu+conf@gmail.com>,   2447410664<2447410664@qq.com>,   saichn<saichn@foxmail.com>,   365088391<365088391@qq.com>,   cleversl<cleversl@126.com>,   syaya0401<syaya0401@163.com>,   yisi22-c<yisi22-c@my.cityu.edu.hk>,   songdi1106<songdi1106@126.com>,   songxiaobin0123<songxiaobin0123@163.com>,   suwangling<suwangling@163.com>,   sunwenzhang<sunwenzhang@mail.dlut.edu.cn>,   sxy1201062<sxy1201062@163.com>,   442064130<442064130@qq.com>,   tanjin802<tanjin802@163.com>,   twhanenao<twhanenao@163.com>,   janlya<janlya@126.com>,   Ty5221<Ty5221@163.com>,   taochunhua<taochunhua@bjtu.edu.cn>,   751252466<751252466@qq.com>,   tongleijing<tongleijing@163.com>,   wanqing_bjtu<wanqing_bjtu@126.com>,   wanpeng168<wanpeng168@126.com>,   wang_charity<wang_charity@163.com>,   wangleiwl<wangleiwl@lzu.edu.cn>,   wangpanna_1<wangpanna_1@163.com>,   wangxi_gogo<wangxi_gogo@163.com>,   wangrouzhi<wangrouzhi@stu.xmu.edu.cn>,   wangtw14<wangtw14@163.com>, jmxyjr<jmxyjr@163.com>,   365274475<365274475@qq.com>,   jin_yu123<jin_yu123@126.com>,   jinxiaocui<jinxiaocui@hpu.edu.cn>,   14110690030<14110690030@fudan.edu.cn>,   1012668471<1012668471@qq.com>,   laishaojuan619<laishaojuan619@163.com>,   liwenfei21<liwenfei21@126.com>,   ali<ali@hust.edu.cn>,   licailingling<licailingling@foxmail.com>,   876404370<876404370@qq.com>,  lg131202<lg131202@163.com>,   492829883<492829883@qq.com>,   372704014<372704014@qq.com>,   lihaoju1990<lihaoju1990@126.com>,   lhongyu525<lhongyu525@126.com>,   huiyunli2011<huiyunli2011@163.com>,   3031538724<3031538724@qq.com>,   lijincai818<lijincai818@163.com>,   779534036<779534036@qq.com>,   queenjing168<queenjing168@hnu.edu.cn>,   like0714<like0714@hnu.edu.cn>,   lilucf<lilucf@163.com>,   liiimeiii<liiimeiii@126.com>,   lipiao_2015<lipiao_2015@163.com>,   shigangli001<shigangli001@163.com>,   523906449<523906449@qq.com>,   liwanlicqu<liwanlicqu@sina.com>,   1154059668<1154059668@qq.com>,   joyinlee<joyinlee@vip.qq.com>,   Lyp211<Lyp211@163.com>,   1052448350<1052448350@qq.com>,   lyq910311<lyq910311@163.com>,   rancylee<rancylee@163.com>,   18435104202<18435104202@163.com>,   18302480869<18302480869@qq.com>,   liaoke<liaoke@whu.edu.cn>,   Linwanfa2013<Linwanfa2013@163.com>,   liuchaoly<liuchaoly@126.com>,   1149810<1149810@qq.com>,   lh92.06.17<lh92.06.17@stu.xjtu.edu.cn>,   heuljj<heuljj@126.com>,   845621045<845621045@qq.com>,   liuq246<liuq246@mail2.sysu.edu.cn>,   cquliuqiang<cquliuqiang@163.com>,   hanemperor<hanemperor@qq.com>,   liuyf102<liuyf102@nenu.edu.cn>,   Liucir9520<Liucir9520@163.com>, bujun<bujun@dufe.edu.cn>,   cai.77<cai.77@163.com>,   caofeng<caofeng@hnu.edu.cn>,   1185601172<1185601172@qq.com>,   yuanyuancao<yuanyuancao@bit.edu.cn>,   369810015<369810015@qq.com>,   530709165<530709165@qq.com>,   cj1125<cj1125@163.com>,   yi.he.xi521<yi.he.xi521@163.com>,   2987047923<2987047923@qq.com>,   chenyx9004<chenyx9004@sina.com>,   18896788276<18896788276@163.com>,   chenzh-2001<chenzh-2001@163.com>,   xdlmh<xdlmh@163.com>,   gltcuijing<gltcuijing@buu.edu.cn>,   hbcuiwen<hbcuiwen@163.com>,   daiyue1980<daiyue1980@163.com>,   dongchengjie<dongchengjie@163.com>,   dongny<dongny@mail.xjtu.edu.cn>,   dongxh45<dongxh45@126.com>,   1184215742<1184215742@qq.com>,   863967036<863967036@qq.com>,   hermione58<hermione58@163.com>,   fshzhpaul<fshzhpaul@163.com>,   gjxuxu<gjxuxu@qq.com>,   1034220210<1034220210@qq.com>,   19767772898<19767772898@qq.com>,  gengyanli1222<gengyanli1222@126.com>,   jingjing_guo<jingjing_guo@163.com>,   549974593<549974593@qq.com>,   hanhongwennl<hanhongwennl@sina.com>,   hanliang828<hanliang828@126.com>,   hyanjin0107<hyanjin0107@sina.cn>,   1056159002<1056159002@qq.com>,   hanahey<hanahey@qq.com>,   HY20170217<HY20170217@126.com>,   zuixiangniande<zuixiangniande@126.com>,   276982058<276982058@qq.com>,   rachel.a.hu<rachel.a.hu@qq.com>,   344684406<344684406@qq.com>,   hjhuang<hjhuang@dbm.ecnu.edu.cn>,   huangjunwei<huangjunwei@hnu.edu.cn>,   huangxiayanok<huangxiayanok@163.com>,   158982753<158982753@qq.com>,   huangz88<huangz88@163.com>,   huangzhh5<huangzhh5@mail2.sysu.edu.cn>,   18724516420<18724516420@163.com>,   jiawanjiao<jiawanjiao@126.com>'

    def get_data(self):
        sql_sel = "SELECT * FROM `member_list`;"
        res_list = self.conn.query(sql_sel)
        for res in res_list:
            # if res['phone_num'] and '.' in res['phone_num']:
            #     update_sql = "UPDATE `member_list` SET phone_num='%s' WHERE email='%s' AND NAME='%s' AND university='%s';"%(res['phone_num'].split('.')[0].replace(' ', ''), res['email'], res['name'], res['university'])
            #     print update_sql
            #     self.conn.execute(update_sql)
            if res['email'] in self.filter_email:
                update_sql = "UPDATE `member_list` SET remark=1 WHERE `NAME`='%s' AND university='%s' AND email='%s';"%(res['name'], res['university'], res['email'])
                print update_sql
                self.conn.execute(update_sql)
                # try:
                #     print update_sql
                #     self.conn.execute(update_sql)
                # except Exception as e:
                #     logging.info(e)
            # session = self.md5(res['name']+u'东北财经大学会计学院'+res['email'])
            # sel_sql = "SELECT * FROM `person_msg` WHERE SESSION = '%s';"%session
            # res_se = self.conn.query(sel_sql)
            # if res_se:
            #     judge = res_se[0]['job_title']
            #     if u'教授' in judge:
            #         continue
            #     if u'博士生导师' in judge:
            #         continue

    def md5(self, str):
        hl = hashlib.md5()
        hl.update(str.encode(encoding='utf-8'))
        return hl.hexdigest()

    def read_xls(self):
        book = xlrd.open_workbook('address.xlsx')
        try:
            sheet = book.sheets()[0]
            nrows = sheet.nrows
            for nrow in xrange(1, nrows):
                name = sheet.cell(nrow, 0).value
                title = sheet.cell(nrow, 1).value
                school = sheet.cell(nrow, 2).value
                number = sheet.cell(nrow, 3).value
                email = sheet.cell(nrow, 4).value
                sel_sql = "SELECT * FROM `member_list` WHERE email='%s';"%(email)
                res = self.conn.query(sel_sql)
                if res:
                    continue
                insert_sql = "INSERT INTO `member_list`(NAME, university, department, main_subject, phone_num, email, remark) VALUES('%s','%s','%s','%s','%s','%s','0');"%(name, school, '', '', number.split('.')[0].replace(' ', ''), email)
                self.conn.execute(insert_sql)
                member_list = self.conn.query(sel_sql)
                if member_list:
                    person_insert_sql = "INSERT INTO `person_msg`(SESSION, NAME, sex, job_title, tutor_category, ethnicity, education, political_face, email, learning_experience, working_experience, research_results, honor) VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');"%(self.md5(name+school+email), name, '', title, '', '', '', '', email, '','','','')
                    self.conn.execute(person_insert_sql)
                print name, title, school, email, number
        except:
            logging.exception('sheet error!')
        return None


if __name__ == '__main__':
    res = op()
    res.get_data()