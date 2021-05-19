#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@Time    :    2020/1/6 0006 12:30
#@Author  :    tb_youth
#@FileName:    MD5.py
#@SoftWare:    PyCharm
#@Blog    :    https://blog.csdn.net/tb_youth

import hashlib


class MD5():
    def __init__(self):
        pass
    # md5加密：结果32位
    def md5Encode(self,s):
        md5 = hashlib.md5()
        md5.update(s.encode(encoding='utf-8'))
        md5_encode = md5.hexdigest()
        return md5_encode