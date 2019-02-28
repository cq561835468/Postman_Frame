#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import logging.config
import sys,time
reload(sys)
sys.setdefaultencoding('utf8')
import threading
import os
import datetime
from Public.public_function import File_Control
from Public.Create_Cmo_Json import Create_Json

logging.config.fileConfig(r'Conf/debug.conf')
logs = logging.getLogger('intest')

class Auto_intest(threading.Thread):
    def __init__(self,device,module,fold_name,path_base,jk_time):
        super(Auto_intest, self).__init__()
        self.device = device #产品名称
        self.Module = module #模块名称
        self.fn = fold_name
        self.path_base = path_base #基准地址
        self.path_module = self.path_base + self.device + '/' + self.Module
        self.jk_time = jk_time

    def Test_Script(self,Module_Name):
        re_list = []
        return_request = FC.GetDir(Module_Name) #单个模块request请求[]
        for rr in return_request:
            '''读取该模块所有请求,返回请求路径'''
            path_run = self.path_module+ '/' + rr
            test_list = FC.Get_Test_Data_List(path_run) #单个reuqest请求脚本和数据
            self.run_test(self.device,self.Module,rr,test_list)
        return re_list

    def run_test(self,device,Module,request_name,test_list):
        '''执行测试用例'''
        FC = File_Control()
        self.now_time = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        self.report_name = device+"#"+Module+"#"+request_name+"#"+self.now_time
        self.report_path = os.getcwd()+'/report/'+self.report_name
        #print test_list[0] 
        len_it = str(FC.json_read_len(test_list[0]))
        #print self.report_pah
        va = "newman run "+test_list[1] +" -n "+len_it +" -d "+ test_list[0] +" -g "+self.path_base+self.device+"/"+self.device+".postman_environment.json"+" -r html,json --reporter-html-export "+self.report_path+".html" + " --reporter-json-export " + self.report_path + ".json"
        #print va
        os.system(va)
        tpp = test_list[1].split('/')
        test_name = tpp[-1]
        tmp = test_list[0].split('/')
        data_name = tmp[-1]
        print "用例为:%s,外部数据为:%s,模块为:%s"%(test_name ,data_name,Module)
        re_cp = "cp "+self.report_path+".html " + self.fn +'/'+self.report_name+".html"
        #print re_cp
        os.system(re_cp)
        logs.debug(u"%s#%s#%s测试完成" % (device,Module,request_name))
        self.CMO_Post(self.device, self.Module, self.report_path+".json", self.report_path+".html", self.now_time, self.jk_time)

    def CMO_Post(self, device, Module, report_path_j, report_path_h, time, jk_time):
        '''发送请求CMO'''
        #print("发送CMO请求")
        #print(report_path_j)
        #print(report_path_h)
        #try:
        CJ = Create_Json(device, Module, report_path_j, report_path_h, time, jk_time)
        CJR = CJ.Run()
        if CJR:
            if CJR["State"]:
               logs.debug(CJR["String"])
            else:
                logs.debug(CJR["String"])
                re_html = "cp " + self.report_path + ".html " + os.getcwd()+"/Cache/" + self.report_name + ".html"
                re_json = "cp " + self.report_path + ".json " + os.getcwd() + "/Cache/" + self.report_name + ".json"
                #print re_html
                os.system(re_html)
                os.system(re_json)

    def run(self):
        self.Test_Script(self.path_module)

def run_list_thread(device,module,fold_name,path_base,jk_time):
    t = Auto_intest(device,module,fold_name,path_base,jk_time)
    t.start()
    #logs.debug("all thread start finish")

if __name__ == '__main__':
    now_time = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    Cacheos = os.getcwd()+"/Cache/" # Cache路径
    path_base = os.path.abspath(os.path.dirname(os.getcwd()))+'/Test_Cases/'
    FC = File_Control()
    '''参数device为产品类型,参数module为执行的接口模块，填all则全部执行'''
    len_module =  len(sys.argv[1:])
    if len_module == 1:
        if sys.argv[0] != "CmoReload":# CMO失败的数据重传
            Cache_path = FC.GetDir(os.getcwd()+"/Cache/")
            for x in Cache_path:
                #print(x+" 重传开始")
                logs.debug("CMO数据重传开始:"+x)
                path = Cacheos + os.path.splitext(x)[0]
                path_spar = path.split("#")
                #print path
                #print path_spar
                CJ = Create_Json(path_spar[0],path_spar[1],path+".json",path+".html", path_spar[2])
                #os.remove(Cache_path + path + ".json")
                #os.remove(Cache_path + path + ".html")
                CJR = CJ.Run()
                if CJR["State"]:
                    #print CJ.Run()
                    logs.debug(CJR["String"])
                    #print(report_path_j)
                    #print(report_path_h)
                    os.remove(path+".json")
                    os.remove(path+".html")
                else:
                    #print CJ.Run()
                    #print(path)
                    logs.debug(CJR["String"])

        else:
            logs.debug(u'缺少具体模块')
    elif len_module == 2:
        device = sys.argv[1] #产品名称
        if sys.argv[2].lower() == 'all': #所有模块用例执行
            FC.del_file()
            fold_name = FC.Mk_fol(os.path.abspath(os.path.dirname(os.getcwd()))+"/report/",now_time+"_"+device)
            Module_Dir = FC.GetDir(path_base + device) # 模块
            #print Module_Dir
            logs.debug(u'测试开始')
            for x in Module_Dir:
                logs.debug(u'项目为 %s,模块为 %s' % (device, x))
                run_list_thread(device,x,fold_name,path_base,now_time)
        elif sys.argv[2].lower() == 'classity': #报告整合
            FC.Getall_htjs_list()
            path = os.getcwd()+'/report/report_classify.html'
            if not os.path.exists(os.path.abspath(os.path.dirname(os.getcwd()))+'/report/t_classify'):
                os.system('mkdir '+os.path.abspath(os.path.dirname(os.getcwd()))+'/report/t_classify')
            cp_report = "cp "+path+" "+os.path.abspath(os.path.dirname(os.getcwd()))+"/report/t_classify/"+now_time+".html"
            #print cp_report
            os.system(cp_report)
        else: #单个模块用例执行
            FC.del_file()
            fold_name = FC.Mk_fol(os.path.abspath(os.path.dirname(os.getcwd()))+"/report/",now_time+"_"+device)
            device,module = sys.argv[1],sys.argv[2]
            logs.debug(u'测试开始')
            logs.debug(u'项目为 %s,模块为 %s' % (device,module))
            run_list_thread(device,module,fold_name,path_base,now_time)
        #time.sleep(300)
        #FC.Getall_htjs_list() #报告整合
    elif len_module == 0:
        logs.debug(u'错误的参数')
    elif len_module > 2: #多个模块用例执行
        FC.del_file()
        fold_name = FC.Mk_fol(os.path.abspath(os.path.dirname(os.getcwd()))+"/report/",now_time+"_"+device)
        device = sys.argv[1]
        logs.debug(u'多个模块')
        logs.debug(u'测试开始')
        for i in sys.argv[2:]:
            logs.debug(u'项目为 %s, 模块为 %s' % (device,i))
            run_list_thread(device,i,fold_name,path_base,now_time)
        #time.sleep(300)
