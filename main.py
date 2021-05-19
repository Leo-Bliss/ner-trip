#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@Time    :    2021/4/18 0018 22:12
#@Author  :    tb_youth
#@FileName:    run.py
#@SoftWare:    PyCharm
#@Blog    :    https://blog.csdn.net/tb_youth


from models.model_manager import ModelManager


if __name__ == '__main__':

    model_mgr = ModelManager()
    # model_mgr.set_model_id('1620921350')
    model_mgr.train()
    # model_mgr.test()
    # model_mgr.input_line_predict()
    # s = '山药'
    # model_mgr.line_predict(s)
    pass
