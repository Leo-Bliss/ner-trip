#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@Time    :    2021/4/18 0018 21:38
#@Author  :    tb_youth
#@FileName:    utils.py
#@SoftWare:    PyCharm
#@Blog    :    https://blog.csdn.net/tb_youth

import sys
import os
from logging import handlers

#### 方便cmd中执行模块找到该模块进行调用#####
cur_path = os.path.abspath(os.path.dirname(__file__))
root_path = os.path.split(cur_path)[0]
sys.path.append(root_path)
############################################

import shutil
import pickle
import logging

from config.setting import PathConfig as path_cfg


DEFAULT_LOG = f'{path_cfg.log_path}/run.log'

def get_logger(log_path=DEFAULT_LOG):
    '''
    日志记录器：控制台+文件handler
    :param log_path:
    :return:
    '''
    logger = logging.getLogger(__name__)
    fmt = logging.Formatter('[%(asctime)s - %(filename)s - %(name)s - %(levelname)s] - %(message)s')
    logger.setLevel(logging.INFO)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(fmt)
    # console_handler.setLevel(logging.INFO)
    logger.addHandler(console_handler)
    # if not os.path.exists(log_path):
    #    create_folder(log_path)
    file_handler = handlers.RotatingFileHandler(filename=log_path, mode='a', maxBytes=40960, backupCount=6,
                                                encoding='utf-8', delay=False)
    # file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(fmt)
    logger.addHandler(file_handler)
    return logger

logger = get_logger() # 全局的logger,其他模块需要使用直接从这里导入

def create_folder(folder_path):
    if os.path.exists(folder_path) or folder_path is None :
        return
    os.makedirs(folder_path)
    logger.info(f'create folders : {folder_path} finished.')

def delete_folder(folder_path):
    if not os.path.exists(folder_path):
        return
    shutil.rmtree(folder_path) # 直接使用shutil模块
    logger.info(f'delete folder : {folder_path} finished.')
    # # 如果使用os模块删除文件夹：文件夹中有文件夹的情况会报错
    # files = os.listdir(folder_path)
    # # 先删除里面文件
    # for file_name in files:
    #     file= f'{folder_path}/{file_name}'
    #     os.remove(file)
    #     print(f'deleted {file} successful!')
    # # 再删除文件夹
    # os.rmdir(folder_path)
    # print(f'deleted {folder_path} successful!')

class EnvManager(object):
    def __init__(self):
        p = path_cfg
        self.floders = [
                   p.extend_data_path,
                   p.process_data_path,
                   p.process_train_data_path,
                   p.process_test_data_path,
                   p.process_pkls_path,
                   p.ckpt_path,
                   p.inputs_path,
                   p.outputs_path
        ]

    def init_floders(self):
        '''
        创建一些必要的文件夹
        :return:
        '''
        logger.info('init folders...')
        for fd in self.floders:
            create_folder(fd)
        logger.info('init folders successfully.')

    def clean_floders(self):
        '''
        清除初始化时创建的文件夹，即回到最初环境
        :return:
        '''
        logger.info('clean folders...')
        for fd in self.floders:
            delete_folder(fd)
        logger.info('clean folders successfully.')

def read_txt_file(src_path):
    with open(src_path, mode='r', encoding='utf-8') as f:
        return f.read()

def read_ann_file(src_path):
    with open(src_path,mode='r',encoding='utf-8') as f:
        return f.readlines()

def read_pkl(src_path):
    with open(src_path,mode='rb') as f:
        return pickle.load(f)

def write_pkl(src_dict,dst_path):
    with open(dst_path,mode='wb') as f:
        pickle.dump(src_dict,f)

class UCharJudge(object):
    # 来源：https://www.cnblogs.com/felixwang2/p/9641379.html
    # 判断一个字符是否为汉字，英文字母，数字，空还是其他
    # 使用Unicode编码来判断
    def __init__(self):
        pass
    @staticmethod
    def is_chinese(uchar):
        """判断一个unicode是否是汉字"""
        if u'\u4e00' <= uchar <= u'\u9fa5':
            return True
        else:
            return False

    @staticmethod
    def is_number(uchar):
        """判断一个unicode是否是数字"""
        if u'\u0030' <= uchar <= u'\u0039':
            return True
        else:
            return False

    @staticmethod
    def is_alphabet(uchar):
        """判断一个unicode是否是英文字母"""
        if (u'\u0041' <= uchar <= u'\u005a') or (u'\u0061' <= uchar <= u'\u007a'):
            return True
        else:
            return False

    @staticmethod
    def is_space(uchar):
        """判断一个unicode是否是空字符串（包括空格，回车，tab）"""
        space = [u'\u0020', u'\u000A', u'\u000D', u'\u0009']
        if uchar in space:
            return True
        else:
            return False



if __name__ == '__main__':
    pass




