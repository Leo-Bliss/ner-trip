#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@Time    :    2021/5/9 0009 16:57
#@Author  :    tb_youth
#@FileName:    count.py
#@SoftWare:    PyCharm
#@Blog    :    https://blog.csdn.net/tb_youth
import os

from preprocess.utils import read_pkl


def t1():
    cls = {'ZH': 13278, 'SX': 2299, 'ZZ': 9520, 'FY': 18969, 'FJ': 1889, 'MX': 1394, 'ZF': 1307}
    for k,v in cls.items():
        path = r'D:\NER\data\TCM\pkls'+f'\\{k}.pkl'
        lst = read_pkl(path)[k]
        print(k,len(lst))

    '''词表统计
    ZH 1589
    SX 103
    ZZ 1771
    FY 6653
    FJ 14819
    MX 108
    ZF 550
    '''


TCM_entities = {'ZH': 13278, 'SX': 2299, 'ZZ': 9520, 'FY': 18969, 'FJ': 1889, 'MX': 1394, 'ZF': 1307}
Mix_entities = {'ZH': 22899, 'SX': 2376, 'ZZ': 15312, 'FY': 22345, 'FJ': 2402, 'MX': 1417, 'ZF': 2792}
Contest_entities = {}
for k, v in Mix_entities.items():
    Contest_entities[k] = Mix_entities[k] - TCM_entities[k]

print(Contest_entities)
'''Contest_entities
{'ZH': 9621, 'SX': 77, 'ZZ': 5792, 'FY': 3376, 'FJ': 513, 'MX': 23, 'ZF': 1485}
'''


'''
绘制柱状图
'''
import matplotlib as mpl

mpl.use('TkAgg')
import matplotlib.pyplot as plt

def pre_count_plot():
    #中文乱码处理
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    cls = ['FY','FJ','ZH','ZF','SX','MX','ZZ']
    #构建数据
    cnt = [Contest_entities[c] for c in cls]

    # plt.figure(figsize=(6, 10))

    #添加标签# #绘图
    # plt.bar(range(len(cnt)),cnt,0.4,color='r',alpha=0.8)

    # plt.ylabel('数量')
    # plt.xlabel('实体类别')

    #添加标题
    # plt.title('实体统计')
    #添加刻度标签

    # plt.xticks(range(len(cnt)),cls)
    # #设置y轴的刻度
    # plt.ylim([10,6300])
    # plt.xticks(rotation=30,fontsize=8)
    # #为每个条形添加数值
    # for x,y in enumerate(cnt):
    #     plt.text(x,y+50,'%s'%y,ha='center')
    # plt.show()


    #水平条形图 ：barh

    #绘图
    plt.barh(range(len(cnt)),cnt,0.4,color='r',alpha=0.8)

    #添加标签
    plt.xlabel('数量')
    plt.ylabel('实体类别')
    #添加标题
    # plt.title('实体统计')
    #添加刻度标签
    plt.yticks(range(len(cnt)),cls,fontsize=8)
    plt.xticks(fontsize=8)
    #设置y轴的刻度
    plt.xlim([0,10800])
    #为每个条形添加数值
    for x,y in enumerate(cnt):
        plt.text(y+500,x,'%s'%y,ha='center',fontsize=8)
    plt.show()

#
# data = read_pkl(r'D:\NER\data\Mix\inputs\test.pkl')
# print(data)
if __name__ == '__main__':
    pre_count_plot()
