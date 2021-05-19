#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@Time    :    2021/4/25 0025 15:51
#@Author  :    tb_youth
#@FileName:    csv_ann.py
#@SoftWare:    PyCharm
#@Blog    :    https://blog.csdn.net/tb_youth
import os

import pandas as pd

def csv2ann():
    FILE_NUM = len([x for x in os.listdir(f'../original') if x.split('.')[-1]=='txt'])
    for i in range(FILE_NUM):
        csv_file = f'../process_csv/{i}.csv'
        df = pd.read_csv(csv_file)
        # print(df.values)
        ann_file = f'../original/{i}.ann'
        with open(ann_file, mode='w', encoding='utf-8') as f:
            for item in df.values:
                id, entity, s, e, content = tuple(item)
                f.write(f'{id}\t{entity} {s} {e}\t{content}\n')
        print(csv_file," transform to ",ann_file,' finished!')

if __name__ == '__main__':
    # csv2ann()
    # from preprocess.data_utils import count_entities
    # count_entities(r'D:\NER\data\TCM\original')
    pass
