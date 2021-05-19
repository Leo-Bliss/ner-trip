#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@Time    :    2021/5/1 0001 5:20
#@Author  :    tb_youth
#@FileName:    count_test.py
#@SoftWare:    PyCharm
#@Blog    :    https://blog.csdn.net/tb_youth


import os

def count_entities(root_path,file_list):
    '''
    从原始数据.ann文件中获取所有实体类型
    :param path: 文件所在路径
    :return:
    '''
    entities_count_dict = {}
    for file in file_list:
        file_path = f'{root_path }/{file}'
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                entity_class = line.split('\t')[1].split(' ')[0]
                if entity_class not in entities_count_dict:
                    entities_count_dict[entity_class] = 1
                else:
                    entities_count_dict[entity_class] += 1
    return entities_count_dict

def count_test_entity():
    path1 = r'D:\NER\data\TCM\process\test'
    test_files = os.listdir(path1)
    test_files = [x.split('.')[0] + '.ann' for x in test_files]
    print(test_files)
    root_path = r'D:\NER\data\TCM\original'
    res_mp = count_entities(root_path,test_files)
    for k,v in res_mp.items():
        print(k,' : ',v)

class Evaluator():
    '''
    传统指标
    '''
    def __init__(self,Nr,Nc,Na,name,rate=1):
        self.Nr = Nr
        self.Nc = Nc
        self.Na = Na
        self.name = name
        self.rate = rate

        self.P = self.calc_P()
        self.R = self.calc_R()
        self.F = self.calc_F()

    def calc_P(self):
        if self.Nc == 0:
            return 0
        return self.Nc/self.Nr * 100

    def calc_R(self):
        assert self.Na>0
        return self.Nc/self.Na * 100

    def calc_F(self):
        r2 = self.rate**2
        up = self.R * self.P * (1 + r2)
        down = self.R + self.P * r2
        return up/down

    def print_evl(self):
        print(f'{self.name} : P = {self.P}, R = {self.R}, F = {self.F}')

class MacroEvaluator():
    '''
    宏平均指标
    '''
    def __init__(self,P_dct,R_dct,rate=1):
        self.P_dct = P_dct
        self.R_dct = R_dct
        self.CN = len(self.P_dct)
        self.rate = rate

        self.macroP = self.calc_macroP()
        self.macroR = self.calc_macro_R()
        self.macroF = self.calc_macro_F()

    def calc_macroP(self):
        return sum(self.P_dct.values())/self.CN

    def calc_macro_R(self):
        return sum(self.R_dct.values())/self.CN

    def calc_macro_F(self):
        r2 = self.rate ** 2
        up = self.macroR * self.macroP * (1 + r2)
        down = self.macroR + self.macroP * r2
        return up / down

    def print_evl(self):
        print(f' Macro-P = {self.macroP}, Macro-R = {self.macroR}, Macro-F = {self.macroF}')

Na_dct = {
    'FJ'  :  326,
    'ZH'  :  2388,
    'ZF'  :  228,
    'ZZ'  :  1827,
    'FY'  :  3236,
    'SX'  :  418,
    'MX'  :  241
      } # 文本中的实体数量
Nr_dct = {
    'FJ'  :  289,
    'ZH'  :  2228,
    'ZF'  :  156,
    'ZZ'  :  1302,
    'FY'  :  3331,
    'SX'  :  295,
    'MX'  :  125
      } # 识别出的实体数量
Nc_dct = {
    'FJ'  :  226,
    'ZH'  :  1564,
    'ZF'  :  93,
    'ZZ'  :  1109,
    'FY'  :  2963,
    'SX'  :  212,
    'MX'  :  83
      } # 识别正确的实体数量


if __name__ == '__main__':
    evls = [Evaluator(Nr_dct[k],Nc_dct[k],Na_dct[k],name=k) for k in Na_dct.keys()]
    P_dct = {}
    R_dct = {}
    for e in evls:
        e.print_evl()
        P_dct[e.name] = e.P
        R_dct[e.name] = e.R
    macro = MacroEvaluator(P_dct,R_dct)
    macro.print_evl()

    pass
    # count_test_entity()
