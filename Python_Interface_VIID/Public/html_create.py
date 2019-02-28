#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup
import time,fcntl,socket,struct,ConfigParser
#import time,socket,ConfigParser
import os

class Create_templte():
    def __init__(self,lists_d):
        self.list_all = sorted(lists_d,key=lambda x:x['collection'])

    def Get_CF(self,session,name):
        '''获取Conf文件内容'''
        cf = ConfigParser.ConfigParser()
        cf.read(os.getcwd()+"/Conf/Conf.conf")
        return cf.get(session, name)

    def Get_Ip(self,ifname):
        '''获取网卡IP'''
        #print ifname
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ip =  socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15]))[20:24])
        #print ip
        return ip

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
            # self.change_test(new_td3, str(Tr['iterations']['failed']))
            self.change_test(new_td3, str(Tr['requests']['total']))
            self.change_test(new_td4, str(Tr['requests']['failed']))
            # self.change_test(new_td5, str(Tr['prerequestScripts']['total']))
            # self.change_test(new_td6, str(Tr['prerequestScripts']['failed']))
            self.change_test(new_td5, str(Tr['testScripts']['total']))
            self.change_test(new_td6, str(Tr['testScripts']['failed']))
            self.change_test(new_td7, str(Tr['assertions']['total']))
            self.change_test(new_td8, str(Tr['assertions']['failed']))
            self.change_test(new_td9, str(round(Tr['responseAverage'],2))+' ms')

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

    def Get_HTMl(self):
        '''获取当前report下html文件数量，用于统计测试用例集总数'''
        arrw = os.listdir(os.getcwd()+r'/report/')
        num = 0
        for x in arrw:
            if '.html' == os.path.splitext(x)[1]:
                num +=1
        return num
        

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
            f_num = float(num)
            dict_value['all_time'] += f_num
        dict_value['all_time'] = round(dict_value['all_time'])
        # print dict_value['all_time']
        #--------------计算平均响应时间--------------------
        eva = 0
        for ev in self.list_all:
            eva += ev['responseAverage']
        if len(self.list_all):
            eva = round(eva/len(self.list_all))
        # --------------计算失败用例、断言数量--------------------
        F_num = 0 #断言
        F_F_num = 0 #用例集
        for TF in self.list_all:
            print TF
            # print TF['iterations']
            # print TF['requests']
            # print TF['prerequestScripts']
            # print TF['testScripts']
            F_num += TF['pf'][1]
            if TF['pf'][1] > 0:
                F_F_num +=1
        # print F_num
        #-----------------循环写入-----------------------
        self.change_test(td_all[1], self.Get_Ip(self.Get_CF("CMO_Conf", "Service_ETH")))  # 执行IP地址
        self.change_test(td_all[3], strTime)   #执行时间
        self.change_test(td_all[5], 'Newman v3.9.4')  # 编译版本
        self.change_test(td_all[7], str(dict_value['all_time'])+'s')  # 总运行时间
        self.change_test(td_all[9], self.k_kb_gb())  # 总运行时间
        self.change_test(td_all[11], str(eva) + 'ms')  # 平均响应时间
        self.change_test(td_all_th[3], str(F_num))  # 失败跌点
        self.change_test(td_all_th[5], str(F_F_num)) # 失败测试集结合
        self.change_test(td_all_th[7], str(self.Get_HTMl()))
        # self.change_test(td_all[9], str(eva) + 'ms')  # 平均响应时间
        self.for_test_result()
        # self.for_test_dec()
        self.new_del_html(self.soup)

if __name__ == "__main__":
    Create_templte().run(r'C:\Users\Administrator\Desktop\xxx~\report\report_0703.html')
