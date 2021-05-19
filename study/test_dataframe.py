#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@Time    :    2021/4/21 0021 7:42
#@Author  :    tb_youth
#@FileName:    test_dataframe.py
#@SoftWare:    PyCharm
#@Blog    :    https://blog.csdn.net/tb_youth

from pandas import DataFrame

data = [
    [1,2,3],[1,5,6],[7,8,9]
]
df = DataFrame(data,columns=['a','b','c'])
print(df)
Exisit = True
print(Exisit in set(df['a']==1))
