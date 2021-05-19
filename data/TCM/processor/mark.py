#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@Time    :    2021/4/23 0023 17:08
#@Author  :    tb_youth
#@FileName:    mark.py
#@SoftWare:    PyCharm
#@Blog    :    https://blog.csdn.net/tb_youth
import multiprocessing
import os

import pandas as pd
import  numpy as np

from preprocess.utils import UCharJudge as ch_judge
from preprocess.utils import write_pkl,read_pkl

def get_split_list(x):
    if x.find('、') != -1:
        return x.split('、')
    if x.find(',') != -1:
        return x.split(',')
    if x.find('，') != -1:
        return x.split('，')
    return []

def exisit_chinese(entity):
    '''
    实体中是否存在中文
    :param entity:
    :return:
    '''
    for x in entity:
        if ch_judge.is_chinese(x):
            return True
    return False

def group_judge(ch):
    '''
    中文 or 英文 or 数字
    :param ch:
    :return:
    '''
    return ch_judge.is_chinese(ch) or ch_judge.is_alphabet(ch) or ch_judge.is_number(ch)


def clear_illegal_entity(entity_list):
    '''
    处理一些不合法的实体
    :param entity_list:
    :return:
    '''
    print('before: ', entity_list)
    tmp = []
    for entity in entity_list:
        if not exisit_chinese(entity):  # 不存在中文
            print('del: ', [entity])
            continue
        # 两边不是中文且不是英文且不是数字则删减
        pre_len = len(entity)
        left = 0
        right = pre_len - 1
        while left <= right:
            del_flag = False
            if not group_judge(entity[left]):
                left += 1
                del_flag = True
            if not group_judge(entity[right]):
                right -= 1
                del_flag = True
            if not del_flag:
                break
        if left <= right:
            tmp.append(entity[left:right+1])
            if right-left+1 < pre_len:
                print('len: ',pre_len,'--->',right-left+1)
                print([entity],' was cut to ',[entity[left:right+1]])
        else:
            print('del: ', [entity])
    print('after: ', tmp)
    return tmp

def get_entity_list(file_path,cnt=0,add=None):
    if  not os.path.exists(file_path):
        return []
    df = pd.read_csv(file_path)
    entity_list = []
    for line in df.values:
        #_, x1, x2 = line
        x1 = line[1]
        x2 = line[-1]
        if not(x1 is  x2): # 侯证和治法只有一列 有效数据
            entity_list.append(x1)
        if isinstance(x2, str):
            x2_split = get_split_list(x2)
            # print('split',x2_split)
            entity_list.extend(x2_split)
    entity_list.sort(key=lambda x: len(x), reverse=True)
    # 处理不合法实体
    entity_list = clear_illegal_entity(entity_list)
    # 干预纠正前cnt个,纠正后的内容在add里面
    while cnt>0:
        entity_list.pop(0)
        cnt -= 1
    if add:
        entity_list.extend(add)
    entity_list = list(set(entity_list))  # 去重
    entity_list.sort(key=lambda x: len(x), reverse=True)
    return entity_list




def build_entity_dict(entity_class,name=None):
    '''
    增加了实体字典，重新整合实体
    :param entity_class:
    :param name:
    :return:
    '''
    file_path = None
    add = None
    cnt = 0
    entity_list = []
    if name is not None:
        ex_file = '../raw_data/extend/'+f'{name}.csv'
        if entity_class == 'ZH': # 此时用上方的/的路径会找不到文件，这样手动动构造路径会有bug!
            ex_file = r'D:\NER\data\TCM\raw_data\extend\证侯.csv'

        df = pd.read_csv(ex_file)['name']
        lst = df.values.tolist()
        lst = clear_illegal_entity(lst)
        entity_list.extend(lst)

    if entity_class == 'FY':
        file_path = r'D:\NER\data\TCM\raw_data\方药（id_名称_别名）.csv'
        add = ['脾瘅', '口甘', '咽干', '烦渴']
        cnt = 1

    elif entity_class == 'FJ':
        file_path = r'D:\NER\data\TCM\raw_data\方剂（id_名称_别名）.csv'
        add = ['寸金丹', '黍米寸金丹', '延寿丹']
        cnt = 2

    elif entity_class == 'ZH':
        file_path = r'D:\NER\data\TCM\raw_data\证候(id_名称).csv'

    elif entity_class == 'ZF':
        file_path = r'D:\NER\data\TCM\raw_data\治法(id_名称).csv'

    if file_path is not None:
        entity_list.extend(get_entity_list(file_path, cnt, add))

    print('final: ', entity_list)

    if entity_class == 'ZH':
        extend_entity = [item[:-2] for item in entity_list if item[-1] == '证']
        entity_list.extend(extend_entity)
        entity_list = list(set(entity_list))
        entity_list.sort(key=lambda x: len(x), reverse=True)
        pass

    entity_list = list(set(entity_list))
    entity_list.sort(key=lambda x:len(x),reverse=True)
    print(len(entity_list),entity_list)
    one = [x  for x in entity_list if len(x)==1]
    print(one)
    entity_list = [x  for x in entity_list if len(x)>1]
    entity_dict = {entity_class:entity_list}
    save_path = f'D:/NER/data/TCM/pkls/{entity_class}.pkl'
    write_pkl(entity_dict,save_path)
    print(entity_class,' dicit write finished.')


def mark_one_txt(txt_path,entity_list,entity_class):
    if len(entity_list) == 0:
        return
    with open(txt_path,mode='r',encoding='utf-8') as f:
        txt = f.read()
        # print(txt)
    mark_list = []
    for item in entity_list:
        cnt = 0
        x = txt.find(item)
        lens = len(item)
        while x != -1:
            cnt += 1
            # print(entity_class,x,x+lens,item) # s,e,entity
            mark_list.append([entity_class,x,x+lens,item])
            x = txt.find(item,x+lens)
        if cnt:
            pass
            # print('*'*100)
    # print(txt_path,entity_class,'Find finished.')
    return mark_list




def mark_all_txt(entity_class):
    FILE_NUM = len([x for x in os.listdir(f'../original') if x.split('.')[-1] == 'txt'])
    path = f'D:/NER/data/TCM/pkls/{entity_class}.pkl'
    entity_list = read_pkl(path)[entity_class]
    if entity_class == 'FY':
        add = ['蜡', '麦', '藕','芜', '汞','蜜','砒','蟾',
                '醋','梨', '米', '桂', '菟', '蛀','栗', '瓢', '茹',
                 '韭', '铅', '蒜',  '椒','枣', '茶','芎', '鸡', '硫',
                 '梅', '芩', '艾', '葱', '麻', '姜','鳔','蛜','酒',
                 '盐', '油', '酥', '矾', '糟', '麝','麸']
        entity_list.extend(add) # 手工加上之前被过滤掉的合理一个字的FY实体
    elif entity_class == 'ZH':
        add = ['暑', '痛', '阳', '风', '亡', '疳', '阴', '冷', '热', '瘀', '虚', '干']
        entity_list.extend(add)
    else:
        pass
    print(entity_class)
    print(len(entity_list),entity_list)
    cpu_cnt = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(cpu_cnt)
    results = []
    for i in range(0,FILE_NUM):
        txt_path = f'../original/{i}.txt'
        res = pool.apply_async(mark_one_txt,args=(txt_path,entity_list,entity_class))
        results.append(res)
        # res = mark_one_txt(txt_path,entity_list,entity_class)
        # print('-'*100)
    pool.close()
    pool.join()
    return [res.get() for res in results]


def build_mark_dict():
    aim = ['FY','FJ','ZH','ZF','MX','SX','ZZ']
    res = []
    for cls in aim:
        sub = mark_all_txt(cls)
        print(sub)
        res.append(sub)

    all_mark = []
    file_num = len(res[0])
    print(file_num)
    for i in range(file_num):
        tmp = []
        for sub in res: # 文件i中的标注的实体sub
            tmp.extend(sub[i])
        all_mark.append(tmp)


    all_mark_dict = {'all_mark': all_mark}
    save_path = '../pkls/all_mark_dict.pkl'
    write_pkl(all_mark_dict,save_path)


if __name__ == '__main__':
    pass
    # build_entity_dict('ZZ','症状')
    # build_mark_dict()
    save_path = '../pkls/all_mark_dict.pkl'
    all_mark = read_pkl(save_path)['all_mark']
    # print(all_mark)
    # print(len(all_mark))
    for i,item in enumerate(all_mark):
       item.sort(key=lambda x: len(x[-1]), reverse=True)
       print(i,item)
       df = pd.DataFrame(data=item,columns=['entity_class','start_pos','end_pos','content'])
       save_path = f'../process_csv/{i}.csv'
       df.to_csv(save_path,encoding='utf-8')




