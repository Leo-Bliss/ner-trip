#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@Time    :    2021/4/30 0030 3:51
#@Author  :    tb_youth
#@FileName:    tmp.py.py
#@SoftWare:    PyCharm
#@Blog    :    https://blog.csdn.net/tb_youth



import json
import os

p = os.path.join(os.getcwd(),'entity.json')
with open(p,mode='r',encoding='utf-8') as f:
    mp = json.loads(f.read())
    print(mp['entity-color'])

