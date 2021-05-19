#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@Time    :    2021/5/9 0009 15:50
#@Author  :    tb_youth
#@FileName:    entity_info_plot.py
#@SoftWare:    PyCharm
#@Blog    :    https://blog.csdn.net/tb_youth



'''
绘制柱状图
'''
import matplotlib as mpl

mpl.use('TkAgg')
import matplotlib.pyplot as plt

#构建数据
cnt = [1016,1133,3257,6090,1718,728,641,71,156,1104,1206,623,14]

#中文乱码处理
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
#
# plt.figure(figsize=(6, 10))


#添加标签# #绘图
# plt.bar(range(len(cnt)),cnt,0.4,color='r',alpha=0.8)

# plt.ylabel('数量')
# plt.xlabel('实体类别')

#添加标题
# plt.title('竞赛数据集实体统计')
#添加刻度标签
cls = ['DRUG_DOSAGE','DRUG_TASTE','DRUG_EFFICACY','SYMPTOM','PERSON_GROUP','DRUG_INGREDIENT',
                              'FOOD_GROUP','FOOD','DRUG','DISEASE','SYNDROME','DISEASE_GROUP','DRUG_GROUP']
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
# plt.ylabel('实体类别')
#添加标题
# plt.title('实体统计')
#添加刻度标签
plt.yticks(range(len(cnt)),cls,fontsize=8,rotation=40)
plt.xticks(fontsize=8)
#设置y轴的刻度
plt.xlim([10,6600])
#为每个条形添加数值
for x,y in enumerate(cnt):
    plt.text(y+260,x,'%s'%y,ha='center',fontsize=8)
plt.show()

# #柱状图和折线图混合使用
#
# sales = [455,885,234,669,999,789,1315]
# plt.rcParams['font.sans-serif'] = ['SimHei']
# plt.rcParams['axes.unicode_minus'] = False
# #绘制折线
# #构建折线图数据
# jan_sales = [123,567,345,987,888,567,233]
# x = ['苹果','香蕉','梨','葡萄','芒果','菠萝','西瓜']
# plt.plot(x,sales,'r',linestyle='--')
# # plt.plot(x,jan_sales,'g',lw=5)
#
# #柱状图
# plt.bar(range(len(sales)),sales,width=0.2,color='b',alpha=0.6) #0.2:柱状宽度，alpha：颜色透明度
# plt.ylabel('销量')
# plt.title('')
# plt.xticks(range(len(sales)),x)
# plt.ylim([100,1500])
# for x,y in enumerate(sales):
#     plt.text(x,y+50,'%s'%y,ha='center')
#
# plt.show()
