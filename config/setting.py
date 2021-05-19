#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@Time    :    2021/4/7 0007 12:04
#@Author  :    tb_youth
#@FileName:    setting.py.py
#@SoftWare:    PyCharm
#@Blog    :    https://blog.csdn.net/tb_youth

'''
采用py脚本作为配置文件，采用类定义配置项，便于使用
'''
import os
import sys

#### 方便cmd中执行模块找到该模块进行调用#####
cur_path = os.path.abspath(os.path.dirname(__file__))
root_path = os.path.split(cur_path)[0]
sys.path.append(root_path)
############################################


class MySqlConfig:
    host = '127.0.0.1'
    port = 3306
    db = 'test'
    username = 'test'
    password = '666'


class PathConfig:
    base_data_path = os.path.join(root_path,'data','Mix')  #f'{root_path}/data/Mix' # 设置数据存放文件夹
    original_data_path = os.path.join(base_data_path,'original') #f'{base_data_path}/original' # 原始数据
    extend_data_path = os.path.join(base_data_path,'extend') #f'{base_data_path}/extend' # 原始数据中提取出的扩展数据
    process_data_path = os.path.join(base_data_path,'process') #f'{base_data_path}/process' # 原始数据经过处理的数据
    process_train_data_path = os.path.join(process_data_path,'train') #f'{process_data_path}/train' # 训练集文件所在路径
    process_test_data_path = os.path.join(process_data_path,'test') #f'{process_data_path}/test' # 测试集文件所在路径
    process_pkls_path = os.path.join(process_data_path,'pkls') #f'{process_data_path}/pkls' # 生成的字典：二进制文件
    log_path = os.path.join(root_path,'logs') #f'{root_path}/logs' # 使用时是相对于需要使用的地方的相对路径:所以这里我引入项目root_path作为参考
    inputs_path = os.path.join(base_data_path,'inputs')
    outputs_path = os.path.join(base_data_path,'outputs')

class EntityConfig:
    # 从original中数据中统计获得
    contest_entities = {  # 共13个类别
        # 实体类别：该类实体数量
        'DRUG_DOSAGE': 1016,  # 药剂
        'DRUG_TASTE': 1133,  # 药味
        'DRUG_EFFICACY': 3257,  # 药性（药物作用）
        'SYMPTOM': 6090,  # 症状
        'PERSON_GROUP': 1718,  # 人群
        'DRUG_INGREDIENT': 728,  # 药物成分
        'FOOD_GROUP': 641,  # 食性（忌【辛辣】）
        'FOOD': 71,  # 食物
        'DRUG': 156,  # 药物(方药？)
        'DISEASE': 1104,  # 疾病
        'SYNDROME': 1206,  # 综合征
        'DISEASE_GROUP': 623,  # 疾病类
        'DRUG_GROUP': 14  # 药物类
    }
    TCM_entities =  {'ZH': 13278, 'SX': 2299, 'ZZ': 9520, 'FY': 18969, 'FJ': 1889, 'MX': 1394, 'ZF': 1307}
    Mix_entities = {'ZH': 22899, 'SX': 2376, 'ZZ': 15312, 'FY': 22345, 'FJ': 2402, 'MX': 1417, 'ZF': 2792}
    new_Mix = {'ZH': 5967, 'MX': 1421, 'SX': 2423, 'ZZ': 17555, 'FY': 22385, 'FJ': 2434, 'ZF': 4180}



