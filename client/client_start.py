#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@Time    :    2021/5/9 0009 0:13
#@Author  :    tb_youth
#@FileName:    client_start.py
#@SoftWare:    PyCharm
#@Blog    :    https://blog.csdn.net/tb_youth

'''
客户端启动入口
'''
import sys
from PyQt5.QtWidgets import QApplication
from NerDemo.main_window import MainWindow


if __name__=='__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())