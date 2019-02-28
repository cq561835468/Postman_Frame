#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os,re,json,time
import socket, fcntl, struct, ConfigParser
from bs4 import BeautifulSoup
from public_function import File_Control
import requests
from suds.client import Client

class Create_Json():
    def __init__(self,Device,Module,JsonFile,HtmlFile,time, jk_time):
        self.Json =File_Control().json_read(JsonFile)
        Html = BeautifulSoup(open(HtmlFile), 'lxml')
        # self.taglist1 = Html.find_all('td') # 获取断言
        self.taglist2 = Html.find_all('div', attrs={'class': re.compile("col-md-6")}) # 通用参数
        # self.taglist3 = Html.find_all('div', attrs={'class': re.compile("col-md-8")}) # 获取后置数值
        # self.taglist4 = Html.find_all('h4', attrs={'class': re.compile("panel-title")}) #获取名字
        # self.taglist5 = Html.find_all('div', attrs={'class': re.compile("col-md-4")})  # 获取前置名称
        taglist6 = Html.find_all('a', attrs={'href': re.compile("#requestData")}) # 请求的标题
        taglist7 = Html.find_all('a', attrs={'href': re.compile("#failureData")})  # 失败的标题
        self.True = [x.text for x in taglist6]
        self.False = [x.text.strip() for x in taglist7]
        self.taglist8 = Html.find_all('div', attrs={'class': re.compile("panel panel-default")})  # 框架
        self.Device = Device
        self.Module = Module
        self.RunTime = time
        self.jk_time = jk_time

    def Get_Ip(self,ifname):
        '''获取网卡IP'''
        #print ifname
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ip =  socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15]))[20:24]) 
        #print ip
        return ip

    def Get_CF(self,session,name):
        '''获取Conf文件内容'''
        cf = ConfigParser.ConfigParser() 
        cf.read(os.getcwd()+"/Conf/Conf.conf")
        return cf.get(session, name)


    def Time_From(self,Value):
        '''处理时间函数转换为秒'''
        time_all = 0
        for i in Value:
            #print i[-1:]
            if 'm' == i[-1:]:
                #print float(i[0:-1])
                time_all += float(i[0:-1])*60
            elif 'ms' == i[-2:]:
                time_all += float(i[0:-2]) /1000
            elif 's' == i[-1]:
                # print float(i[0:-1])
                time_all += float(i[0:-1])
        return time_all

    def Run(self):
        if self.Get_CF("CMO_Conf","Open_ID") == "0":
            return False
        li = self .Public_Table()
        Js_Data = self.Request_Table(li)
	return_state = {"State":False,"String":""}
        print(Js_Data)
        try:
            if self.Post_CMO(Js_Data):
                return_state["State"] = True
                return_state["String"] = "CMO接口返回数据成功"
                return return_state
            return_state["String"] = "CMO接口返回数据错误"
            return return_state
        except:      
            return_state["String"] = "CMO接口异常"
            return return_state

    def Public_Table(self):
        '''表1，通用数据'''
        Re_Data = {}
        Re_Data['Jenkins_Time'] = self.jk_time # jenkins同步时间
        Re_Data['Project'] = self.Device # 产品名称
        Re_Data['Module'] = self.Module # 模块名称
        Re_Data['Collection'] = self.Json['collection']['info']['name'] # 测试用例集名字
        Re_Data['Time'] = self.RunTime  # 开始时间
        Re_Data['Exported with'] = "Newman v3.10.0"  # 开始时间
        Re_Data['Iterations'] = self.Json['run']['stats']['iterations'] # 迭代信息
        Re_Data['Requests'] = self.Json['run']['stats']['requests'] # 请求信息
        Re_Data['Assertions'] = self.Json['run']['stats']['assertions'] # 断言信息
        Re_Data['TestScripts'] = self.Json['run']['stats']['testScripts'] # 测试用例信息
        Re_Data['PrerequestScripts'] = self.Json['run']['stats']['prerequestScripts'] # 前置脚本信息
        # Re_Data['method'] = self.Json['run']['executions'][0]['request']['method'] # 请求类型
        Re_Data['Total_run_duration'] = self.Time_From(str(self.taglist2[1].text).split(' ')) # 总运行时间
        Re_Data['Total_data_received'] = str(self.Json['run']['transfers']['responseTotal']) +'B' # 传输数据大小
        Re_Data['Average_response_time'] = str(self.Json['run']['timings']['responseAverage']) +"ms" # 平均响应时间
        Re_Data['Total_Failures'] = int(self.taglist2[-1].text)  # 总失败断言数
        #print self.Get_Ip("CMO_Conf",self.Get_CF("CMO_Conf", "Service_ETH"))
        Re_Data['Service_IP'] = self.Get_Ip(self.Get_CF("CMO_Conf", "Service_ETH"))  # IP地址
        #Re_Data['Service_IP'] = '172.16.120.20'
        return Re_Data
        # js = json.dumps(Re_Data, sort_keys=True, indent=4, separators=(',', ':'))
        # print(js)

    def Request_Table(self, li):
        '''表2，请求数据'''
        Failures = []
        Parent_Product = []
        List_All = li
        for x in self.taglist8:
            #print "-----------------------------"
            a = x.find_all('h4')
            #print a[0].text.strip()
            if a[0].text.strip() in self.True:
                # self.Request_Detail(x,a[0].text.strip())
                Parent_Product.append(self.Request_Detail(x,a[0].text.strip()))
            else:
                Failures.append(self.False_Detail(x,a[0].text.strip()))
        List_All["Failures"] = Failures
        List_All["Parent_Product"] = Parent_Product
        #print List_All
        return List_All

    def Request_Detail(self, frame, name):
        '''处理请求的数组内容'''
        list_tmp = {}
        list_tmp["Name"] = name
        cm4 = frame.find_all('div', attrs={'class': re.compile("col-md-4")})  # 获取前置名称
        cm8 = frame.find_all('div', attrs={'class': re.compile("col-md-8")})  # 获取后置名称
        for index,value in enumerate(cm4):
            if value.text == "Tests":
                list_tmp[value.text] = self.assert_Detail(cm8[index])
            else:
                list_tmp[value.text] = cm8[index].text
        js = json.dumps(list_tmp, sort_keys=True, indent=4, separators=(',', ':'))
        #print list_tmp
        return list_tmp

    def assert_Detail(self, Test_Value):
        '''处理断言内容'''
        arrw = []
        val = Test_Value.find_all('td')
        for x in range(0,len(val),3):
            list = {}
            list["Name"] = val[x].text
            list["Pass_count"] = val[x+1].text
            list["Fail_count"] = val[x+2].text
            arrw.append(list)
        return arrw

    def False_Detail(self, frame, name):
        """处理失败内容表"""
        list_tmp = {}
        list_tmp["Name"] = name
        cm4 = frame.find_all('div', attrs={'class': re.compile("col-md-4")})  # 获取前置名称
        cm8 = frame.find_all('div', attrs={'class': re.compile("col-md-8")})  # 获取后置名称
        for index,value in enumerate(cm4):
            list_tmp[value.text] = cm8[index].text
        js = json.dumps(list_tmp, sort_keys=True, indent=4, separators=(',', ':'))
        #print js
        return list_tmp

    def Post_CMO(self, data):
        """发送数据给CMO系统"""
        datas = json.dumps(data)
        url = self.Get_CF("CMO_Conf", "Service_Url")
        #url = "http://172.16.6.147:8001/testinginfo/getinfo/?wsdl" 
        #print url
        test = Client(url)
        re = test.service.Testing_Result(datas)
        print "-" * 20
        print re[0]
        print "-" * 20
        return re


if __name__ == "__main__":
    time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    Device = "PJ"
    Module = "Area"
    path = os.path.dirname(os.getcwd())
    JF = path+"/report/PJ#Area#DELETE_CODE#2019-01-29_09:24:39.json"
    HF = path+"/report/PJ#Area#DELETE_CODE#2019-01-29_09:24:39.html"
    CJ = Create_Json(Device,Module,JF,HF,time)
    CJ.Run()
    #print  CJ.Get_Ip("ens160")
