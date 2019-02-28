#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from public_function import File_Control
from bs4 import BeautifulSoup,os,re
import json

class Req_Resp():
    '''解析newman的json文件内容'''
    def __init__(self,path):
        self.json_path = path

    def Get_NameID(self,json):
        '''获取执行结果所有name和ID'''
        ar = {}
        for x in json["collection"]["item"]:
            # li = {}
            ar[x["name"]] = {x["id"]:[]}
            # ar.append(li)
        return ar

    def Get_RR(self,Json, NameList):
        List_Re = {}
        O_Str_Request = ''
        O_Str_Response = ''
        Arrw_Request = []
        Arrw_Response = []
        for value in Json["run"]["executions"]:
            List_Tmp = {}
            List_Tmp["Request_Body"] = self.Back_Def(self.Get_Request_Body, value)
            List_Tmp["Request_Head"] = self.Back_Def(self.Get_Request_Head, value).replace(u'\n','\r')
            List_Tmp["Response_Body"] = self.Back_Def(self.Get_Response_Body, value)
            List_Tmp["Response_Head"] = self.Back_Def(self.Get_Response_Head, value)
            # print list(NameList.keys()) [NameList.values().index(value["id"])]
            for x in NameList.values():
                # print x
                # print x.keys()[0]
                if value["id"] == x.keys()[0]:
                    x[value["id"]].append(List_Tmp)
        for xx in NameList:
            arrw_tmp = []
            # print xx
            #print NameList[xx]
            for x in NameList[xx].values():
                NameList[xx] = x
                #print json.dumps(x, sort_keys=True, indent=4, separators=(',', ':'))
        return NameList

    def Get_Request_Head(self,json):
        try:
            head = ''
            for x in json["request"]["header"]:
                val = "%s:%s\n" % (x["key"],x["value"])
                head += val
        except:
            head = ''
        finally:
            return head

    def Get_Request_Body(self,json):
        try:
            body = json["request"]["body"]["raw"]
        except:
            body = ''
        finally:
            return body

    def Get_Response_Head(self, json):
        try:
            head = ''
            for x in json["response"]["header"]:
                val = "%s:%s\n" % (x["key"],x["value"])
                head += val
        except:
            for x in json["requestError"]["errno"]:
                head += x
        finally:
            return head

    def Get_Response_Body(self, json):
        try:
            body = ''
            for x in json["response"]["stream"]["data"]:
                body += chr(x)
        except:
            for x in json["requestError"]["errno"]:
                body += x
        finally:
            return body

    def Back_Def(self,val1,val2):
        return val1(val2)

    def run(self):
        FC = File_Control()
        FC_JSON = FC.json_read(self.json_path)
        Item_Arrw = self.Back_Def(self.Get_NameID,FC_JSON)
        #print Item_Arrw
        Re_Value = self.Get_RR(FC_JSON,Item_Arrw)
        #print json.dumps(Re_Value, sort_keys=True, indent=4, separators=(',', ':'))
        return Re_Value

class Html_RR():
    '''写入html详情中body和request'''
    def __init__(self,Json_Data,Html_Path):
        self.Json_Data = Json_Data
        self.Html_Path = Html_Path
        self.soup = BeautifulSoup(open(self.Html_Path), 'lxml')

    def new_del_html(self,soup):
        '''写入文件'''
        f = open(self.Html_Path,'w')
        f.write(str(soup))
        f.close()

    def Tag_Insert(self,tag,Obj,classes=None,text=None):
        '''写入页面控件'''
        Tr1 = self.soup.new_tag(tag)
        if classes:
            Tr1['class'] = classes
        if text:
            Tr1.string = text
        Obj.append(Tr1)
        return Tr1

    def Class_FindIn(self,className,Div,Obj):
        '''查找控件'''
        arrw = Obj.find_all(Div, attrs={'class': re.compile(className)})
        return arrw


    def run(self):
        print
        Tag1 = self.Class_FindIn('panel-group', 'div', self.soup)
        for y in range(0,len(self.Json_Data)):
            x = Tag1[y]
            title = self.Class_FindIn('', 'h4', x)[0].text# 标题
            data = self.Json_Data[title]  # 数据
            #print json.dumps(data, sort_keys=True, indent=4, separators=(',', ':'))
            for d in data:
                body = self.Class_FindIn('panel-body', 'div', x)[0]  # body体
                # -----------------request------------------------
                self.Tag_Insert('hr', body, 'col-md-11') #插入hr
                RH = self.Tag_Insert('div', body, 'col-md-12')
                self.Tag_Insert('b', RH, text='Request')
                self.Tag_Insert('hr', body, 'col-md-11')  # 插入hr
                self.Tag_Insert('pre', body, text=d['Request_Head'], classes="col-md-12")
                self.Tag_Insert('pre', body, text=d['Request_Body'], classes="col-md-12")
                # -----------------response------------------------
                self.Tag_Insert('hr', body, 'col-md-11')  # 插入hr
                RH = self.Tag_Insert('div', body, 'col-md-12')
                self.Tag_Insert('b', RH, text='Response')
                self.Tag_Insert('hr', body, 'col-md-11')  # 插入hr
                self.Tag_Insert('pre', body, text=d['Response_Head'], classes="col-md-12")
                self.Tag_Insert('pre', body, text=d['Response_Body'], classes="col-md-12")
        self.new_del_html(self.soup)


if __name__ == "__main__":
    RP = Req_Resp(r"A:\svn\interface_test\Postman_Auto\Python_Interface_VIID\report\hh.json")
    RP.run()
    #FC_JSON = FC.json_read(r"A:\svn\interface_test\Postman_Auto\Python_Interface_VIID\report\hh.json")
    #print(FC_JSON["run"]["executions"][0]["response"]["stream"]["data"])
    # for value in FC_JSON["run"]["executions"]:
    #     #print value
    #     O_Str = ''
    #     for value_resp in value["response"]["stream"]["data"]:
    #         if isinstance(str((chr(value_resp))),str):
    #             O_Str += str((chr(value_resp)))
    #     print O_Str
    # O_Str_Request = ''
    # O_Str_Response = ''
    # for value in FC_JSON["run"]["executions"]:
    #     O_Str_Request = value["request"]["body"]["raw"]
    #     # print value["request"]["header"]
    #     head = ''
    #     for x in value["request"]["header"]:
    #         val = "%s:%s\n" % (x["key"],x["value"])
    #         head += val
    #     #print head
    #     # print O_Str_Request
    #     O_Str_Response = value["response"]["stream"]["data"]
    #     print O_Str_Response


    # print("head为%s,body为%s" % (head,O_Str_Request))
        # print value["response"]
        # print value["request"]
        # O_Str_Request = value["request"]
        # O_Str_Response = value["Response"]
        # print O_Str_Request
        # print O_Str_Response
