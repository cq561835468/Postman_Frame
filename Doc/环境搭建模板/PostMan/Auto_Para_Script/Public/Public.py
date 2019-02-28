#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import xlrd
import json
import os
import sys
import codecs
#reload(sys)
#sys.setdefaultencoding('utf-8')

def Find_excel():
    arrw = []
    for root,dirs,filename in os.walk('/opt/PostMan/Postman_Auto/Auto_Para_Script/Global_Json/'):
        for files in filename:
            if 'xlsx' in files:
                arrw.append([root,files])
    return arrw


class Csv_Pro():
    def __init__(self,file_xlsx):
        self.path = file_xlsx[0]+'/' #输出路径
        self.file_xlsx = file_xlsx[0]+'/'+file_xlsx[1] #excel路径
        self.file_name = file_xlsx[1].split('.')[0]
        #xlrd.Book.encoding = "utf-8"
        self.table = xlrd.open_workbook(self.file_xlsx)
        self.page = self.table.sheet_names()#excel sheet列表
        #print self.file_name

    def Write_Json(self,data,path):
        '''写入json文件'''
        f = codecs.open(path,'w+','utf-8')
        f.write(json.dumps(data, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ':')))
        f.close()

    def run(self):
        list_re = {}
        for name in self.page:
            list_tmp = []
            sheel = self.table.sheet_by_name(name)
            #print sheel.nrows
            for num in range(0,sheel.nrows):
                dict_tmp = {}
                if num == 0:
                    Key_Arrw = []
                    Key_Arrw_IS = []
                    Key_Arrw_Sort = sheel.row_values(num)
                    for s in Key_Arrw_Sort:
                        sp = s.split('|')
                        Key_Arrw.append(sp[0])
                        Key_Arrw_IS.append(sp[1])
                else:
                    Value_Arrw = sheel.row_values(num)
                    for num_two in range(0,len(Key_Arrw_IS)):
                        #print Value_Arrw[num_two]
                        #print type(Value_Arrw[num_two])
                        if Key_Arrw_IS[num_two] == 'int':
                            Value_Arrw[num_two] = int(Value_Arrw[num_two])
                        elif Key_Arrw_IS[num_two] == 'str':
                            if isinstance(Value_Arrw[num_two],float):
                                Value_Arrw[num_two] = str(int(Value_Arrw[num_two]))
                            else:
                                Value_Arrw[num_two] = Value_Arrw[num_two]
                        #elif Key_Arrw_IS[num_two] == 'istr':
                            #Value_Arrw[num_two] = str(int(Value_Arrw[num_two]))
                    dict_tmp = dict(zip(Key_Arrw,Value_Arrw))
                    list_tmp.append(dict_tmp)
            #print list_tmp
            list_re[name] = list_tmp
        #print list_re
        print u"excel处理完成"
        self.Write_Json(list_re,self.path+self.file_name+'.json')


            #print sheel.row_values(0)
        

if __name__ == "__main__":
    arrw = Find_excel()
    for x in arrw:
        print x
        CP = Csv_Pro(x)
        CP.run()
