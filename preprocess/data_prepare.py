#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@Time    :    2021/4/19 0019 23:06
#@Author  :    tb_youth
#@FileName:    data_prepare.py
#@SoftWare:    PyCharm
#@Blog    :    https://blog.csdn.net/tb_youth


from preprocess.data_utils import show_entities, process_multi_files, show_entities, get_fetures_dict
from config.setting import PathConfig as path_config
# from preprocess.data_utils import build_data # 有其他特征
from preprocess.processor import build_data, build_word2id  # 无其他特征

from preprocess.utils import EnvManager

if __name__ == '__main__':

    pass
## step1 ：在config.setting中设置你数据存放的base_data_path,然后在下面创建original_data_path，将数据放到下面
## ----------------------------------------------------------------
# # stpe2: 执行初始化文件夹环境代码
#     env_mrg = EnvManager()
#     # env_mrg.clean_floders()
#     env_mrg.init_floders()
## ----------------------------------------------------------------
## step3: 统计一下目标实体，对目标实体以及数据集有个大概了解
    # show_entities()
## ----------------------------------------------------------------
# step4: 构建特征数据集，将根据划分放入process_data_path下的训练（train），测试(test)文件夹中
#     process_multi_files()
## step5: 构建字符词典和处理好数据集并写入pkl文件

    # print(get_fetures_dict())
    # build_word2id() # 单独提取出词对应的id字典
    # build_data(file_path=path_config.process_train_data_path,name='train',augmentation=False)
    # build_data(file_path=path_config.process_test_data_path,name='test')
## step6: train,test ...



