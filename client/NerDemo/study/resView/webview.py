#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@Time    :    2021/4/28 0028 14:18
#@Author  :    tb_youth
#@FileName:    webview.py
#@SoftWare:    PyCharm
#@Blog    :    https://blog.csdn.net/tb_youth


from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import sys
import os

class WebEngnieViewDemo(QMainWindow):
    def __init__(self):
        super(WebEngnieViewDemo,self).__init__()
        self.setWindowTitle('打开外部网页')
        self.setGeometry(5,50,1335,730)
        self.browser = QWebEngineView()
        #在线html页面
        # self.url = QUrl(r"https://www.csdn.net/")
        # self.browser.load(self.url)

        # 本地html页面
        url = r'D:\Learn-python-notes\projects\demo\NerDemo\study\resView\1.html'
        self.browser.load(QUrl.fromLocalFile(url))
        self.setCentralWidget(self.browser)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WebEngnieViewDemo()
    window.show()
    sys.exit(app.exec_())