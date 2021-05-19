#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@Time    :    2021/5/10 0010 4:07
#@Author  :    tb_youth
#@FileName:    plot2.py
#@SoftWare:    PyCharm
#@Blog    :    https://blog.csdn.net/tb_youth


'''
绘制折线图
'''
import matplotlib as mpl

mpl.use('TkAgg')


import matplotlib.pyplot as plt

data1 = [71.00,83.74,85.71,82.76,68.14]
data2 = [33.94,52.78,53.30,48.92,11.30]
data3 = [45.93,64.75,65.73,61.49,19.38]
#中文乱码处理
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

x = ['0.1','0.01','0.001','0.0001','0.00001']

plt.plot(x,data1,marker='^',color='g',lw=1,linestyle='--',label='Macro-P')
plt.plot(x,data2,marker='o',color='y',lw=1,linestyle='--',label='Macro-R')
plt.plot(x,data3,marker='*',color='b',lw=1,linestyle='--',label='Macro-F')
#label显示
plt.legend()

#x轴标签
plt.xticks(x)

# plt.title('学习率调参')

plt.ylim(5,100)

#标上数值
for x,y in enumerate(data1):
    plt.text(x,y+2,'%s'%y,ha='center')

for x,y in enumerate(data2):
    plt.text(x,y+2,'%s'%y,ha='center')

for x,y in enumerate(data3):
    plt.text(x,y+2,'%s'%y,ha='center')
# #图的保存，一定要放在show之前
# plt.savefig(r'./images/polyLine.png')
#保存为矢量图
#plt.savefig(r'./images/example1.svg',dpi=600,format='svg')
plt.show()

