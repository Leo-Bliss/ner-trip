#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@Time    :    2021/5/1 0001 7:32
#@Author  :    tb_youth
#@FileName:    res_plot.py
#@SoftWare:    PyCharm
#@Blog    :    https://blog.csdn.net/tb_youth



import matplotlib as mpl

mpl.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np

#防止中文乱码
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


names = (u'识别出的实体数量', u'识别对的实体数量')
Nr_dct = {
    'FY'  :  2414,
    'FJ'  :  251,
    'ZH'  :  1782,
    'ZF'  :  196,
    'SX'  :  315,
    'MX'  :  200,
     'ZZ': 1322
      } # 识别出的实体数量
Nc_dct = {
    'FY'  :  2242,
    'FJ'  :  197,
    'ZH'  :  1568,
    'ZF'  :  137,
    'SX'  :  287,
    'MX'  :  187,
    'ZZ'  :  1536
      } # 识别正确的实体数量
keys = Nr_dct.keys()
values = (Nr_dct.values(), Nc_dct.values())


# 设置柱形图宽度
bar_width = 0.35

index = np.arange(len(values[0]))
# 绘制第一个柱形
rects1 = plt.bar(index, values[0], bar_width, color='#0072BC', label=names[0])
# 绘制第二个柱形
rects2 = plt.bar(index + bar_width, values[1], bar_width, color='#ED1C24', label=names[1])
# X轴标题
plt.xticks(index + bar_width/2, keys)
# Y轴范围
plt.ylim(ymax=3500, ymin=0)
# 图表标题
# plt.title(u'NER结果')
# 图例显示
plt.legend(loc='upper left')

# 添加数据标签
def add_labels(rects):
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width()/2, height, height, ha='center', va='bottom',fontsize=8)
        # 柱形图边缘用白色填充，纯粹为了美观
        rect.set_edgecolor('white')

add_labels(rects1)
add_labels(rects2)

plt.show()

# # 图表输出到本地
# plt.savefig('values_par.png')