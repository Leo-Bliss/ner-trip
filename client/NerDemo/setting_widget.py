#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@Time    :    2021/4/30 0030 4:38
#@Author  :    tb_youth
#@FileName:    setting_widget.py
#@SoftWare:    PyCharm
#@Blog    :    https://blog.csdn.net/tb_youth
import sys

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QApplication, QTextEdit, QPushButton


class SettingWidget(QWidget):
    addr_sender = pyqtSignal(tuple)
    def __init__(self):
        super(SettingWidget,self).__init__()
        self.initUI()

    def initUI(self):
        self.ip_label = QLabel('服务器  IP:')
        self.ip_line_edit = QLineEdit('127.0.0.1')
        self.ip_line_edit.setPlaceholderText('默认为local')
        self.port_label = QLabel('服务器端口:')
        self.port_line_edit = QLineEdit()
        self.port_line_edit.setText('8888')

        hlayout1 = QHBoxLayout()
        hlayout1.addWidget(self.ip_label)
        hlayout1.addWidget(self.ip_line_edit)
        hlayout2 = QHBoxLayout()
        hlayout2.addWidget(self.port_label)
        hlayout2.addWidget(self.port_line_edit)
        # self.test_link_label = QLabel('连接结果：【RES】')
        # self.test_link_label.hide()
        self.test_conn_btn = QPushButton('连接')
        self.save_btn = QPushButton('保存')
        hlayout3 = QHBoxLayout()
        hlayout3.addStretch(0)
        # hlayout3.addWidget(self.test_link_label)
        hlayout3.addWidget(self.test_conn_btn)
        hlayout3.addWidget(self.save_btn)
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText('Connection Information..')
        self.text_edit.setStyleSheet('QTextEdit{font-size:20px;}')

        vlayout = QVBoxLayout()
        vlayout.addLayout(hlayout1)
        vlayout.addLayout(hlayout2)
        vlayout.addLayout(hlayout3)
        vlayout.addWidget(self.text_edit)

        self.setLayout(vlayout)

        self.test_conn_btn.clicked.connect(self.onClinckedConnect)

    def showConnectInfo(self,info):
        self.text_edit.append(info)

    def onClinckedConnect(self):
        ip = self.ip_line_edit.text()
        port = int(self.port_line_edit.text())
        addr = (ip,port)
        self.addr_sender.emit(addr)



if __name__=='__main__':
    app = QApplication(sys.argv)
    window = SettingWidget()
    window.show()
    sys.exit(app.exec_())


