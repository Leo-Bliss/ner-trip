#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@Time    :    2021/4/23 0023 19:05
#@Author  :    tb_youth
#@FileName:    process_excel.py
#@SoftWare:    PyCharm
#@Blog    :    https://blog.csdn.net/tb_youth


from preprocess.excel_helper import ExcelHelper
import pandas as pd
import numpy as np

def write_txt(txt,id):
    file_path = f'../original/{id}.txt'
    with open(file_path,mode='w',encoding='utf-8') as f:
        f.write(txt)
    print(file_path,' write finished.')



def csv2txt(csv_path,start_id=0):
    helper = ExcelHelper()
    data = helper.read_excel(csv_path)
    # 将表格中数据转换成一段文本
    for id, line in enumerate(data):
        s = ''
        for i, item in enumerate(line):
            # print(i, item)
            if i < 1 or len(item) == 0: # 记录id和空内容直接不要
                continue
            s += item
            if item[-1] not in [',', '，', '.', '。', '?', '!', ';']:
                s += '。'  # 没有间隔时，每个字段之间用'。'隔开
        print(len(s), s)
        write_txt(s,id+start_id)
    return len(data)+start_id


def read_extend_excel(path):
    dfs = pd.read_excel(path,sheet_name=None)
    aim_columns = ['脉诊', '舌诊', '一般情况', '望诊', '闻诊', '查体',
       '理化检查', '补充诊查', '中医诊断', '西医诊断', '症候结论', '症结与病势', '治疗原则',
	   '治疗步骤', '其他治疗','处方名称','治疗效果','现病史', '自诉', '代诉','主诉']
    for df in dfs.values():
        data = df[aim_columns].values
        for line in data:
            s = ''
            for item in line:
                print(item)
                if item is np.nan:
                    continue
                tmp = item
                if not isinstance(item,str):
                    tmp = str(item)
                s += tmp

            with open('./tmp.txt',mode='w',encoding='utf-8') as f:
                f.write(s)

            print('='*100)
            print(len(s))
            print(s)
            break
        break





if __name__=='__main__':
    # 暂时不用新的电子病历数据
    # file = r'D:\NER\data\TCM\raw_data\extend\发热和咳嗽疾病的转好电子病历.xlsx'
    # read_extend_excel(file)
    pass
    start_id = 0
    path = r'../raw_data/【aim】古今名家验案全析.csv'
    start_id = csv2txt(path, start_id)
    print('$'*100)
    print(start_id)
    path = r'../raw_data/【aim】中医脾胃病学核对稿20201110.csv'
    start_id = csv2txt(path,start_id)
    print(start_id)





