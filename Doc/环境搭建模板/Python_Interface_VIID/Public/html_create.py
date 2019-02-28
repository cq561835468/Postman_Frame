#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup
import time
import os

class Create_templte():
    def __init__(self,lists_d):
        self.list_all = sorted(lists_d,key=lambda x:x['collection'])

    def k_kb_gb(self):
        '''kb、gb、k转换'''
        list_tmp = 0
        for i in self.list_all:
            if i['Pack_Size'][-2:] == 'KB':
                list_tmp += float(i['Pack_Size'][:-2]) * 1024
            elif i['Pack_Size'][-1:] == 'B':
                list_tmp += float(i['Pack_Size'][:-1])
        Str = '%.2f' % (list_tmp / 1024)
        return Str + 'B'

    def for_test_result(self):
        '''循环写入测试结果'''
        td_all_tbody = self.soup.findAll("tbody")
        for Tr in self.list_all:
            new_tr_tag = self.soup.new_tag('tr')
            td_all_tbody[1].append(new_tr_tag)
            new_td1 = self.soup.new_tag('td')
            new_td2 = self.soup.new_tag('td')
            new_td3 = self.soup.new_tag('td')
            new_td4 = self.soup.new_tag('td')
            new_td5 = self.soup.new_tag('td')
            new_td6 = self.soup.new_tag('td')
            new_td7 = self.soup.new_tag('td')
            new_td8 = self.soup.new_tag('td')
            new_td9 = self.soup.new_tag('td')
            new_td10 = self.soup.new_tag('td')
            new_td11 = self.soup.new_tag('td')
            list1 = [new_td1,new_td2,new_td3,new_td4,new_td5,new_td6,new_td7,new_td8,new_td9,new_td10,new_td11]
            # list2 = [Tr['collection'].encode('utf-8'),str(Tr['iterations']['total']),str(Tr['iterations']['failed']),
            #          str(Tr['requests']['total']),str(Tr['requests']['failed']),str(Tr['prerequestScripts']['total']),
            #          str(Tr['prerequestScripts']['failed']),str(Tr['testScripts']['total']),str(Tr['testScripts']['failed']),
            #          str(Tr['assertions']['total']),str(Tr['assertions']['failed'])]
            for key,value in enumerate(list1):
                new_tr_tag.insert(key, list1[key])
            self.change_test(new_td1, Tr['collection'].encode('utf-8'))
            self.change_test(new_td2, str(Tr['iterations']['total']))
            self.change_test(new_td3, str(Tr['iterations']['failed']))
            self.change_test(new_td4, str(Tr['requests']['total']))
            self.change_test(new_td5, str(Tr['requests']['failed']))
            self.change_test(new_td6, str(Tr['prerequestScripts']['total']))
            self.change_test(new_td7, str(Tr['prerequestScripts']['failed']))
            self.change_test(new_td8, str(Tr['testScripts']['total']))
            self.change_test(new_td9, str(Tr['testScripts']['failed']))
            self.change_test(new_td10, str(Tr['assertions']['total']))
            self.change_test(new_td11, str(Tr['assertions']['failed']))

    def for_test_dec(self):
        '''循环写入测试详情'''
        td_all_tbody = self.soup.findAll("tbody")
        for Tr in self.list_all:
            new_tr_tag = self.soup.new_tag('tr')
            td_all_tbody[2].append(new_tr_tag)
            new_td1 = self.soup.new_tag('td')
            new_td2 = self.soup.new_tag('td')
            new_td3 = self.soup.new_tag('td')
            new_td4 = self.soup.new_tag('td')
            new_td5 = self.soup.new_tag('td')
            new_td6 = self.soup.new_tag('td')
            new_td7 = self.soup.new_tag('td')
            list1 = [new_td1,new_td2,new_td3,new_td4,new_td5,new_td6,new_td7]
            # list2 = [Tr['collection'].encode('utf-8'),str(Tr['iterations']['total']),str(Tr['iterations']['failed']),
            #          str(Tr['requests']['total']),str(Tr['requests']['failed']),str(Tr['prerequestScripts']['total']),
            #          str(Tr['prerequestScripts']['failed']),str(Tr['testScripts']['total']),str(Tr['testScripts']['failed']),
            #          str(Tr['assertions']['total']),str(Tr['assertions']['failed'])]
            for key,value in enumerate(list1):
                new_tr_tag.insert(key, list1[key])
            #print Tr['collection']
            self.change_test(new_td1, Tr['collection'].encode('utf-8'))
            self.change_test(new_td2, str(Tr['method']))
            self.change_test(new_td3, str(Tr['responseAverage'])+'ms')
            self.change_test(new_td4, str(Tr['Pack_Size']))
            self.change_test(new_td5, str(Tr['pf'][0]))
            self.change_test(new_td6, str(Tr['pf'][1]))
            self.change_test(new_td7, str(Tr['state_code']))

    def new_del_html(self,soup):
        '''写入文件'''
        f = open(os.getcwd()+r'/report/report_classify.html','w')
        f.write(str(soup))
        f.close()

    def change_test(self,Obj,value):
        '''更新数据'''
        Obj.string = value

    def run(self):
        dict_value = {}
        self.soup = BeautifulSoup(open(os.getcwd()+r'/Conf/report.html'), 'lxml')
        td_all = self.soup.findAll("td")
        td_all_th = self.soup.findAll("th")

        timeStruct = time.localtime(time.time())
        strTime = time.strftime("%Y-%m-%d %H:%M:%S", timeStruct)
        dict_value['all_time'] = 0
        #-------------计算总运算时间------
        for i in self.list_all:
            num = i['all_time']
            print num
            f_num = float(num)
            dict_value['all_time'] += f_num
        #--------------计算平均响应时间--------------------
        eva = 0
        for ev in self.list_all:
            eva += ev['responseAverage']
        eva = eva/len(self.list_all)
        # --------------计算失败用例时间--------------------
        F_num = 0
        for TF in self.list_all:
            #print TF['pf']
            #print TF['iterations']
            #print TF['requests']
            #print TF['prerequestScripts']
            #print TF['testScripts']
            F_num += TF['pf'][1]
        #-----------------循环写入-----------------------
        # for Tr in self.list_all:
            #print Tr['collection']
            #print Tr['iterations']
            #print Tr['iterations']['total']
            #aTr = u"tr><td width=\"20%\">"+Tr['collection']+"</td><td>"+str(Tr['iterations']['total'])+"</td><td class=\"red\">"+str(Tr['iterations']['failed'])+u"</td><td>"+str(Tr['requests']['total'])+u"</td><td class=\"red\">"+str(Tr['requests']['failed'])+u"</td><td>"+str(Tr['prerequestScripts']['total'])+"</td><td class=\"red\">"+str(Tr['prerequestScripts']['failed'])+"</td><td>"+str(Tr['testScripts']['total'])+"</td><td class=\"red\">"+str(Tr['testScripts']['total'])+"</td><td>"+str(Tr['assertions']['total'])+"</td><td class=\"red\">"+str(Tr['assertions']['failed'])+"</td></tr"

        #------------------------------------------------
        self.change_test(td_all[1], strTime)   #执行时间
        self.change_test(td_all[3], 'Newman v3.9.4')  # 编译版本
        self.change_test(td_all[5], str(dict_value['all_time'])+'s')  # 总运行时间
        self.change_test(td_all[7], self.k_kb_gb())  # 总运行时间
        self.change_test(td_all[9], str(eva)+'ms')  # 平均响应时间
        self.change_test(td_all_th[3], str(F_num))  # 失败测试节点
        self.change_test(td_all[9], str(eva) + 'ms')  # 平均响应时间
        self.for_test_result()
        self.for_test_dec()
        # for i,v in enumerate(td_all):
        #     print i,v
        # for s,a in enumerate(td_all_th):
        #     print s,a
        # for t,p in enumerate(td_all_tbody):
        #     print t,p

        # new_li_tag = soup.new_tag(u"<tr><td width=\"20%\">单个图像数据CRD消息-测试长度测试长度测试长度测试长度测试长度测试长</td><td>1</td><td class=\"red\">0</td><td>1</td><td class=\"red\">0</td><td>1</td><td class=\"red\">0</td><td>2</td><td class=\"red\">0</td><td>3</td><td class=\"red\">3</td></tr>")
        # td_all_tbody[1].append(new_li_tag)
        self.new_del_html(self.soup)

if __name__ == "__main__":
    Create_templte().run(r'C:\Users\Administrator\Desktop\xxx~\report\report_0703.html')
