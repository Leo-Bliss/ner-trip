#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@Time    :    2021/5/13 0013 21:11
#@Author  :    tb_youth
#@FileName:    build_dict.py
#@SoftWare:    PyCharm
#@Blog    :    https://blog.csdn.net/tb_youth


'''
构建词表
'''
import os
import pickle
import pandas as pd


def read_pkl(src_path):
    with open(src_path,mode='rb') as f:
        return pickle.load(f)

def write_pkl(src_dict,dst_path):
    with open(dst_path,mode='wb') as f:
        pickle.dump(src_dict,f)

def get_more_dct():
    base= r'D:\NER\data\mark_self'
    files = os.listdir(r'D:\NER\data\mark_self')
    dct = {}
    for file in files:
        path = os.path.join(base,file)
        df = pd.read_csv(path)
        cls = list(df['entity_class'])
        ct = list(df['content'])
        for i in range(len(cls)):
            # print(cls[i],ct[i])
            if cls[i] in dct:
                dct[cls[i]].append(ct[i])
            else:
                dct[cls[i]] = [ct[i]]
    return dct


def rebuild_dct():
    base = r'D:\NER\data\TCM\pkls'
    e_class = ['FJ', 'FY', 'MX', 'SX', 'ZF', 'ZH', 'ZZ']
    dct = get_more_dct()
    for e in e_class:
        dct_file = os.path.join(base, f'{e}.pkl')
        entity_list = read_pkl(dct_file)[e]
        print(e,len(entity_list))
        print(dct[e])
        if dct[e]:
            entity_list.extend(dct[e])
            entity_list = list(set(entity_list))
        print(e, len(entity_list))
        save_dct = {e:entity_list}
        write_pkl(save_dct,dct_file)
        print('write ',dct_file,' Done')





if __name__ == '__main__':
    rebuild_dct()
    # get_more_dct()
    pass



