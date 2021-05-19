#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@Time    :    2021/4/28 0028 15:52
#@Author  :    tb_youth
#@FileName:    buildjs.py
#@SoftWare:    PyCharm
#@Blog    :    https://blog.csdn.net/tb_youth


left = 'var leftdata = ['

right = 'var rightdata = ['

for i in range(20):
    left += '{'+'text:"文字{}",'.format(i)+'color:"yellow"},'
left += '];'
print(left)
for i in range(10):
    right += '{'+'text:"文字{}",'.format(i)+'color:"blue"},'
right += '];'

file = './test_data.js'
with open(file,mode='w',encoding='utf-8') as f:
    f.write(left)
    f.write('\n')
    f.write(right)