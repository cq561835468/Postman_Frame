#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import json
import time
import datetime
from HTMLParser import HTMLParser
from bs4 import BeautifulSoup
import re
from html_create import Create_templte as CT

class File_Control():
    def Mk_fol(self,base,path):
        mk = base+path
        #print(mk)
        os_mk = "mkdir "+mk
        os.system(os_mk)
        return mk

    def GetDir(self, path):
        '''获取该设备所有模块/获取该模块下所有请求'''
        list_dir = []
        dirs = os.listdir(path)
        for i in dirs:
            #print i
            #print os.path.splitext(i)[1]
            if os.path.splitext(i)[1] != '.json' and i != '.svn':
                list_dir.append(i)
        return list_dir

    def GetTestDir(self, path):
        '''获取文件夹下的具体文件'''
        listarrw = os.listdir(path)
        if ".svn" in listarrw:
	    listarrw.remove(".svn")
        return listarrw

    def Get_Test_Data_List(self,TestDir):
        '''筛选文件josn和_data，优先csv'''
        data_name = None
        test_name = None
        #print TestDir
        TestDirs = self.GetTestDir(TestDir)
        #print TestDirs
        for t in TestDirs:
            if '.csv' in t:
                data_name = t
            else:
                tmp = t.split('.')
                if tmp[-1] == 'json' and tmp[-2][-5:] == '_data' and data_name == None and tmp[-2] != 'conf':
                    #print tmp[-2]
                    #print t
                    data_name = t
                elif tmp[-2][-5:] != '_data' and tmp[-2] != 'conf':
                    test_name = t
        #print TestDir
        #print "%s,%s,%s"%(data_name ,test_name,self.path_module)
        #print data_name
        #print test_name
        return [TestDir + '/' +data_name, TestDir + '/' + test_name]

    def Html_Get(self,path):
        soup = BeautifulSoup(open(path), 'lxml')
        taglist1 = soup.find_all('td')
        taglist2 = soup.find_all('div', attrs={'class': re.compile("col-md-6")})
        taglist3 = soup.find_all('div', attrs={'class': re.compile("col-md-8")})
        list1 = {}
        list_tmp = []
        for i in range(0, len(taglist1) / 3):
            staglist1 = (str(taglist1[i * 3 + 1]).replace('<td>','')).replace('</td>','')
            staglist2 = (str(taglist1[i * 3 + 2]).replace('<td>', '')).replace('</td>', '')
            list_tmp.append([staglist1,staglist2])
        p, f = 0, 0
        for s in list_tmp:
            p +=int(s[0])
            f +=int(s[1])
        list1['pf'] = [p,f]
        a = str(taglist2[1].text).split(' ')
        time_all = 0
        #print a
        for i in a:
            #print i[-1:]
            if 'm' == i[-1:]:
                #print float(i[0:-1])
                time_all += float(i[0:-1])*60
            elif 'ms' == i[-2:]:
                time_all += float(i[0:-2]) /1000
            elif 's' == i[-1]:
                #print float(i[0:-1])
                time_all += float(i[0:-1])
            #print time_all
        list1['all_time'] = time_all
        #list1['method'] = taglist3[0].text
        list1['state_code'] = taglist3[6].text
        list1['Pack_Size'] = taglist3[3].text
        return list1
    def json_read(self,path):
        '''转为json格式处理'''
        with open(path, 'r') as load_f:
            load_dict = json.load(load_f)
        with open(path, 'w') as load_fs:
            json.dump(load_dict,load_fs)
        return load_dict

    def json_read_len(self, path):
        '''统计外部数据长度，用于迭代'''
        with open(path, 'r') as load_f:
            load_dict = json.load(load_f)
        #print load_dict
        with open(path, 'w') as load_fs:
            json.dump(load_dict,load_fs)
        #print load_dict
        return len(load_dict)

    def json_list(self,data_s):
        json_data = data_s + '.json'
        html_data = data_s + '.html'
        #print json_data
        #print html_data
        #a = json_data.split('.')
        #if a[-1] != 'json':
            #json_data,html_data = html_data,json_data
        #print json_data
        #print html_data
        '''处理json数据'''
        load_dict = self.json_read(json_data)
        returnlist = {}
        '''Newman编译版本'''
        #returnlist['Exported_with'] = 'Newman v3.9.4'
        '''测试用例集'''
        returnlist['collection'] = load_dict['collection']['info']['name']
        '''迭代次数、请求、断言、测试脚本、请求前缀'''
        returnlist['iterations'] = load_dict['run']['stats']['iterations']
        returnlist['requests'] = load_dict['run']['stats']['requests']
        returnlist['assertions'] = load_dict['run']['stats']['assertions']
        returnlist['testScripts'] = load_dict['run']['stats']['testScripts']
        returnlist['prerequestScripts'] = load_dict['run']['stats']['prerequestScripts']
        returnlist['method'] = load_dict['run']['executions'][0]['request']['method']
        #print load_dict['run']['executions'][0]['request']['method']
        '''开始时间、结束时间、平均响应时间'''
        #started_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(load_dict['run']['timings']['started'] / 1000))
        #returnlist['started_time'] = started_time
        returnlist['responseAverage'] = load_dict['run']['timings']['responseAverage']
        '''请求类型、平均请求时间、平均请求包大小、状态码'''
        #-------------------------
        re_js = self.Html_Get(html_data)
        returnlist['pf'] = re_js['pf']
        returnlist['all_time'] = re_js['all_time']
        #returnlist['method'] = re_js['method']
        returnlist['state_code'] = re_js['state_code']
        returnlist['Pack_Size'] = re_js['Pack_Size']
        return returnlist
    def Getall_htjs_list(self):
        '''主处理函数'''
        path = os.getcwd() + r'/report'
        #print path
        list_R = []
        list1 = self.GetTestDir(path)
        list_sr = []
        for si in list1:
            list_sr.append(si[0:-5])
        size_list = list(set(list_sr))
        for i in size_list:
            paths = path + '/' + i
            #print paths
            path_json = self.json_list(paths)
            list_R.append(path_json)
        CT(list_R).run()

    def del_file(self):
        #print os.getcwd()
        path = os.getcwd() + r'/report'
        for i in os.listdir(path):
            path_file = os.path.join(path, i) #取文件绝对路径
            if os.path.isfile(path_file):
                os.remove(path_file)
            else:
                pass

if __name__ == '__main__':
    #path_html = r'C:\Users\Administrator\Desktop\xxx~\report\VIID#Batch_Subscriptions#POST#2018-07-03_09_11_53.html'
    #path_json = r'C:\Users\Administrator\Desktop\xxx~\report\VIID#Batch_Subscriptions#POST#2018-07-03_09_11_53.json'
    #path = r'C:\Users\Administrator\Desktop\xxx~\report'
    #test_data = File_Control().Getall_htjs_list(path)
    File_Control().del_file()



    # for key in test_data2:
    #     print key,test_data2[key]
    # soup = BeautifulSoup(open(path),'lxml')
    # # print soup.div.text
    # # name1 = soup.select('.col-md-3')
    # # name2 = soup.select('.col-md-4')
    # # name3 = soup.select('.col-md-6')
    # taglist1 = soup.find_all('td')
    # list = []
    # for i in range(0,len(taglist1)/3):
    #     list.append(taglist1[i*3+1:i*3+2])
        # print taglist1[4:6]
        # print taglist1[7:9]
    # for i in taglist1:
    #     print i
    # for i in taglist1:
    #     print i.text
    # taglist2 = soup.find_all('div', attrs={'class': re.compile("col-md-4")})
    # for ii in taglist2:
    #     print ii.text
    # taglist3 = soup.find_all('div', attrs={'class': re.compile("col-md-6")})
    # for iii in taglist3:
    #     print iii.text
    # list4 = []
    # taglist4 = soup.find_all('div', attrs={'class': re.compile("col-md-8")})
    # for iiii in taglist4:
    #     if iiii.text:
    #         list4.append(iiii.text)
    #
    # print list4
    # for i in list4:
    #     print i
