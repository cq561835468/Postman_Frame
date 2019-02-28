#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import json
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from Public.Public import Csv_Pro,Find_excel

class AutoGet():
    def __init__(self):
        pass

    def del_file(self):
        '''清空tmp目录'''
        path = os.getcwd() + r'/Global_Json_tmp'
        for i in os.listdir(path):
            path_file = os.path.join(path, i) #取文件绝对路径
            if os.path.isfile(path_file):
                os.remove(path_file)
            else:
                print u"无该文件"

    def json_read(self,path):
        '''转为json格式处理'''
        paths = path
        print path
        with open(paths, 'r') as load_f:
            load_dict = json.load(load_f)
        with open(paths, 'w') as load_fs:
            json.dump(load_dict,load_fs)
        return load_dict

    def Json_Data_Completion(self,dict):
        '''用例补全'''
        max_len = []
        for key in dict:
            max_len.append(len(dict[key]))
        for key in dict:
            if len(dict[key]) < max(max_len):
                print u"%s中的%s 参数数量不足，进行补全" % (self.path,key)
                for i in range(len(dict[key]),max(max_len)):
                    dict[key].append(dict[key][i-1])
        return dict

    def Json_Dict_Sp(self,dict_sp):
        '''已补全完毕,input进行拼接'''
        list_tmp =[]
        for num in range(0,len(dict_sp[0])):
            dict_tmp = {}
            for i in dict_sp:
                for sa in i[num]:
                    dict_tmp[sa] = i[num][sa]
            list_tmp.append(dict_tmp)
        return list_tmp

    def Json_Dict_Sp_All(self,input,output):
        '''output和input进行拼接'''
        list_re = []
        for i in input:
            dict_tmp = {}
            for key in i:
                dict_tmp[key] = i[key]
            for keys in output[0]:
                dict_tmp[keys] = output[0][keys]
            list_re.append(dict_tmp)
        return list_re

    def json_write(self,data,path):
        '''写入json文件'''
        f = open(path,'w')
        f.write(json.dumps(data, sort_keys=True, indent=4, separators=(',', ':')))
        f.close()

    def GetTestDir(self, path):
        '''获取文件夹下的所有文件'''
        for root, dirs, filename in os.walk(path):
            pass
        return filename

    def Get_TestDIR_File(self,path):
        '''获取文件夹和其子文件夹下的所有文件'''
        list_re = []
        for root, dirs, filename in os.walk(path):
            list_tmp = []
            if 'conf.json' in filename:#有conf.json才获取地址
                list_tmp.append(root+'/conf.json') #先把conf放进去
                for s in filename:
                    if s != 'conf.json':#不为conf.json的文件
                        file_list = s.split('.') #分割
                        if file_list[-1] == 'json' and file_list[-2][-5:] == '_data': #测试数据
                            os.system("rm -rf "+ s)  #删除该data文件
                        elif file_list[-1] == 'json' and file_list[-2][-5:] !='_data': #测试脚本
                            list_tmp.append(root+'/'+s[0:-5]+'_data.json')#增加与json测试用例相同的名称用于生成测试用
                list_re.append(list_tmp)
            else:#无conf.json则不生成参数脚本
                pass
            #if list_tmp: #如果不为空则代表里面有conf并且文件夹中无data文件
                #list_re.append(list_tmp)
            #print "root is %s" % root
            #print "dirs is %s" % dirs
            #print "filename is %s" % filename
        return list_re

    def GetTestDir_All(self, path, device,module):
        '''获取该产品的模块下的conf文件'''
        path_base = os.path.abspath(os.path.dirname(os.getcwd()))+'/Test_Cases/'
        if not os.path.exists(path_base+device):
            print u"无该产品,请重试"
            return 0
        if module == 'all': #所有模块参数化"
            Re_List = self.Get_TestDIR_File(path_base+device)
        else: #单个模块参数化
            if not os.path.exists(path_base+device+'/'+module):
                print u"无该模块,请重试"
                return 0
            Re_List = self.Get_TestDIR_File(path_base+device+'/'+module)#返回单个模块所有conf文件路径
        return Re_List

    def Analysis_Conf(self,list_data):
        '''解析Conf-触发备份功能-返回用例路径'''
        dir_name = list_data.split('.')
        Test,para = dir_name[0],dir_name[1]
        tmp_path = self.json_tmp_path(Test+'.json')
        js_conf = self.json_read(os.getcwd()+'/'+tmp_path) #读取用例
        return js_conf[para]

    def Move_CP_File(self,path,filename):
        '''复制测试用例到临时目录'''
        path_src = path + '/' + filename
        path_dst = os.getcwd()+ '/Global_Json_tmp'+'/'+ filename
        f = open(path_src, "rb").read()
        open(path_dst, "wb").write(f)
        return '/Global_Json_tmp'+'/'+ filename

    def json_tmp_path(self,path):
        '''备份需要使用到的原始测试用例，放入tmp下'''
        path_in = os.getcwd()+'/Global_Json/InPut'
        path_out = os.getcwd() + '/Global_Json/OutPut'
        list1 = self.GetTestDir(path_in)  # 列出文件夹下所有的目录与文件
        list2 = self.GetTestDir(path_out)  # 列出文件夹下所有的目录与文件
        if path in list1:
            #print path_in,path
            tmp_path = self.Move_CP_File(path_in, path)
            return tmp_path
        elif path in list2:
            #print path_out,path
            tmp_path = self.Move_CP_File(path_out, path)
            return tmp_path
        else:
            print u"[%s]参数名错误,input和output中都无该参数名" % path

    def json_ans(self,path,filename_data):
        self.path = path
        #
        '''单个conf文件的处理方法、'''
        self.del_file() #清空临时文件
        dict_input = {} #输入字典
        dict_output = {} #输出字典
        list_input = [] #输入列表
        list_output = []  # 输出列表
        js_conf = self.json_read(self.path)
        print js_conf
        input_js = js_conf['input_parameter']
        output_js =  js_conf['output_parameter']
        for i in input_js: #分析变量给出返回值 
            dict_input[i] = self.Analysis_Conf(i)
        for s in output_js:#分析变量给出返回值
            dict_output[s] = self.Analysis_Conf(s)
        re_json_input = self.Json_Data_Completion(dict_input)  #用例补全
        for i in re_json_input:
            list_input.append(re_json_input[i])   #放入列表
        for key in dict_output:
            list_output.append(dict_output[key]) #放入输出列表
        input_sp = self.Json_Dict_Sp(list_input)  #input拼接
        out_sp = self.Json_Dict_Sp(list_output)  # output拼接
        all_sp = self.Json_Dict_Sp_All(input_sp,out_sp)
        self.json_write(all_sp,filename_data)
        print "%s 参数化完成,已生成外部数据" % self.path 


if __name__ == "__main__":
    '''产品名 模块名(all)'''
    arrw = Find_excel()
    for x in arrw:
        CP = Csv_Pro(x)
        CP.run()
    #try:
    Device,Module = sys.argv[1],sys.argv[2]
    Need_Para = AutoGet().GetTestDir_All(os.path.abspath(os.path.dirname(os.getcwd()))+'/Test_Cases',Device,Module)
    if not Need_Para:
        print "无需要参数化的模块,脚本结束"
    else:
        print "开始参数化"
        #print Need_Para
        for x in Need_Para:
            #print x
            AutoGet().json_ans(x[0],x[1])
    #except Exception, e:
        #print e
