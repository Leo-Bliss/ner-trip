#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@Time    :    2021/5/8 0008 1:53
#@Author  :    tb_youth
#@FileName:    processor.py
#@SoftWare:    PyCharm
#@Blog    :    https://blog.csdn.net/tb_youth


import os
import pandas as pd

from preprocess.utils import read_pkl,write_pkl
from preprocess.data_utils import DataAugmentation
from config.setting import PathConfig as path_cfg


def build_tag2label():
    '''
    tag2id
    :return:
    '''
    entity_class = ['FY', 'FJ', 'ZH', 'ZZ', 'SX', 'MX', 'ZF']
    mark_items = ['B', 'I', 'E', 'S','O']
    tags = ['O']
    for entity in entity_class:
        for m in mark_items:
            if m == 'O':
                continue
            tag = f'{m}-{entity}'
            tags.append(tag)
    id2tag = {}
    tag2id = {}
    for id, tag in enumerate(tags):
       id2tag[id] = tag
       tag2id[tag] = id
    print(id2tag)
    print(tag2id)



def build_word2id():
    fet_dict_path = os.path.join(path_cfg.process_pkls_path,'fetures_dict.pkl')
    dct = read_pkl(fet_dict_path)
    word2id = dct['word'][1]
    print(word2id)
    dst_path = os.path.join(path_cfg.base_data_path,'inputs','word2id.pkl')
    write_pkl(word2id,dst_path)


def build_data(file_path,name='train',augmentation=False):
    files = os.listdir(file_path)
    data = []
    for file in files:
        path = os.path.join(file_path, file)
        df = pd.read_csv(path, encoding='utf-8')
        w = df['word'].tolist()
        tag = df['label'].tolist()
        seg_w,seg_tag = [],[]
        for i in range(len(w)):
            if w[i] != 'seg':
                seg_w.append(w[i])
                seg_tag.append(tag[i])
            else:
                if len(seg_w):
                    data.append((seg_w,seg_tag))
                else:
                   pass
                seg_w, seg_tag = [], []
    if augmentation:
        da = DataAugmentation()
        pass

    data_dict = {name:data}
    file_name = f'{name}.pkl'
    base = os.path.join(path_cfg.base_data_path,'inputs')
    if not os.path.exists(base):
        os.makedirs(base)
    path = os.path.join(base,file_name)
    write_pkl(data_dict,path)
    print(f'save: {path} --- finished')


def bioes2bio(mark_data):
    ans = []
    for item in mark_data:
        tmp = [item[0]]
        if item[-1][0] == 'S':
            tmp.append('B' + item[-1][1:])
        elif item[-1][0] == 'E':
            tmp.append('I' + item[-1][1:])
        else:
            tmp.append(item[-1])
        ans.append(tmp)
    return ans


def get_mark_list(mark_data):
    length = len(mark_data)
    if length == 0:
        return
    left = 0
    mark_list = []
    while left < length:
        while left < length and mark_data[left][-1][0] != 'B':
            left += 1
        content = ''
        if left < length:
            content += mark_data[left][0]
        else:
            break
        entity = mark_data[left][-1][2:]
        right = left + 1
        while right < length and mark_data[right][-1][0] == 'I' and mark_data[right][-1][2:] == entity:
            content += mark_data[right][0]
            right += 1
        start_pos, end_pos = left, right
        mark_list.append([entity, start_pos, end_pos, content])
        left = right
    return mark_list



if __name__ == '__main__':
    # test_path = path_cfg.process_test_data_path
    # train_path = path_cfg.process_train_data_path
    # build_data(test_path,'test')
    # build_data(train_path, 'train')
    # build_word2id()
    # res = read_pkl(r'E:\project\ChineseNer\zh-NER-TF\data_path\Mix\pkls\fetures_dict.pkl')
    # print(res)
    pass
    # build_tag2label()