#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@Time    :    2021/5/6 0006 22:45
#@Author  :    tb_youth
#@FileName:    rebuild_data.py
#@SoftWare:    PyCharm
#@Blog    :    https://blog.csdn.net/tb_youth
import multiprocessing
import os
import shutil
import pandas as pd

from preprocess.utils import read_pkl, write_pkl

''''
处理竞赛数据集中的目标实体
'''

def copy_files():
    '''
    复制竞赛数据集
    :return:
    '''
    ctst = [x for x in os.listdir(r'D:\NER\data\Contest\original') if x.split('.')[-1] == 'txt']
    emr = [x for x in os.listdir(r'D:\NER\data\TCM\original') if x.split('.')[-1] == 'txt']
    start_id = len(emr)
    frm = r'D:\NER\data\Contest\original'
    to = r'D:\NER\data\Mix\original'
    for src in ctst:
        old = os.path.join(frm, src)
        dst = str(start_id) + '.txt'
        new = os.path.join(to, dst)
        start_id += 1
        print(old, '---------->', new)
        shutil.copyfile(old, new)

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



def mark_all_txt(entity_class,txts_path,dct_path):
    txt_files = [x for x in os.listdir(txts_path) if x.split('.')[-1] == 'txt']
    path = f'{dct_path}/{entity_class}.pkl'
    entity_list = read_pkl(path)[entity_class]
    if entity_class == 'FY':
        add = ['蜡', '麦', '藕','芜', '汞','蜜','砒','蟾',
                '醋','梨', '米', '桂', '菟', '蛀','栗', '瓢', '茹',
                 '韭', '铅', '蒜',  '椒','枣', '茶','芎', '鸡', '硫',
                 '梅', '芩', '艾', '葱', '麻', '姜','鳔','蛜','酒',
                 '盐', '油', '酥', '矾', '糟', '麝','麸']
        entity_list.extend(add) # 手工加上之前被过滤掉的合理一个字的FY实体
    # elif entity_class == 'ZH':
    #     add = ['暑',  '阳', '风', '亡', '疳', '阴', '冷', '热', '瘀', '虚']
    #     entity_list.extend(add)
    else:
        pass
    print(entity_class)
    print(len(entity_list),entity_list)
    cpu_cnt = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(cpu_cnt)
    results = []
    for file_name in txt_files:
        txt_path = os.path.join(txts_path,file_name)
        res = pool.apply_async(mark_one_txt,args=(txt_path,entity_list,entity_class))
        results.append(res)
        # res = mark_one_txt(txt_path,entity_list,entity_class)
        # print('-'*100)
    pool.close()
    pool.join()
    return [res.get() for res in results]

def build_mark_dict(txts_path,dct_path,save_path):
    aim = ['FY','FJ','ZH','ZF','MX','SX','ZZ']
    res = []
    for cls in aim:
        sub = mark_all_txt(cls,txts_path,dct_path)
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
    write_pkl(all_mark_dict,save_path)


def csv2ann(csvs_path,ann_path):
    csv_files = [x for x in os.listdir(csvs_path) if x.split('.')[-1] == 'csv']
    for file in csv_files:
        csv_file = os.path.join(csvs_path,file)
        df = pd.read_csv(csv_file)
        # print(df.values)
        name = str(file.split('.')[0]) + '.ann'
        ann_file = os.path.join(ann_path,name)
        with open(ann_file, mode='w', encoding='utf-8') as f:
            for item in df.values:
                id, entity, s, e, content = tuple(item)
                f.write(f'{id}\t{entity} {s} {e}\t{content}\n')
        print(csv_file," transform to ",ann_file,' finished!')

if __name__ == '__main__':
    txts_path = r'D:\NER\data\Mix\original' # txt源文本
    dct_path = r'D:/NER/data/TCM/pkls' # 词表
    # FJ : 感冒 感觉不是合法的，但是FJ词表中有
    # ZF : 貌似与功效差不多
    # SX,MX 在竞赛数据集中几乎没有
    # t = mark_all_txt('ZZ',txts_path,dct_path)
    # print(t)

    save_path = r'D:\NER\data\Mix\pkls\all_mark_dict.pkl' # 每个文件标注结果保存路径
    ## first
    # build_mark_dict(txts_path, dct_path, save_path)
    all_mark = read_pkl(save_path)['all_mark']
    print('@@@ : ',len(all_mark))
    # print(all_mark)
    ## second
    # for i,item in enumerate(all_mark):
    #    item.sort(key=lambda x: len(x[-1]), reverse=True)
    #    print(item)
    #    df = pd.DataFrame(data=item,columns=['entity_class','start_pos','end_pos','content'])
    #    path = r'D:\NER\data\Mix\process_scv'
    #    save_path = os.path.join(path,str(i)+'.csv')
    #    df.to_csv(save_path,encoding='utf-8')
    ## third
    csv_path = r'D:\NER\data\Mix\process_scv'
    ann_path = r'D:\NER\data\Mix\original'
    csv2ann(csv_path,ann_path)
    pass

