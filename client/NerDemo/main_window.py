#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@Time    :    2021/4/22 0022 0:01
#@Author  :    tb_youth
#@FileName:    main_window.py
#@SoftWare:    PyCharm
#@Blog    :    https://blog.csdn.net/tb_youth

import sys
import os
import time
import socket
import json

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QApplication, QStyleFactory,QStackedWidget

from PyQt5.QtWidgets import QHBoxLayout

from NerDemo.ner_widget import NerWidget
from NerDemo.setting_widget import SettingWidget
from NerDemo.tree_widget import TreeWidget
from NerDemo.about_widget import AboutWidget
from NerDemo.home_widget import HomeWidget
from NerDemo.data_center import DataCenterWidget

from NerDemo.mark_widget import MarkWidget
from NerDemo.utils import CommonHelper as comm
from net.utils import MsgContainer

CUR_PATH = os.path.abspath(os.path.dirname(__file__))


class WorkThread(QThread):
    finished = pyqtSignal()
    ner_mklst_sender = pyqtSignal(list)
    mc = MsgContainer(5)
    def __init__(self,src,client):
        super().__init__()
        self.data = src
        self.client = client

    def run(self):
        print(len(self.data))
        self.client.send(self.mc.pack_data(self.data))
        ans = ''
        while True:
            rcv = self.client.recv(1024)
            if len(rcv) == 0 or rcv is None:
                break
            self.mc.add_data(rcv)
            if len(self.mc.get_all_msg()):
                ans = self.mc.get_all_msg()[0]
                break
        self.mc.clear_all_msg()
        # write ans to js file
        ans = json.loads(ans)['ans']
        print(len(self.data),len(ans))
        mark_data = [[self.data[i], ans[i]] for i in range(len(self.data))]
        mark_data = comm.bioes2bio(mark_data)
        mark_list = comm.get_mark_list(mark_data)
        view = comm.build_view(mark_data,mark_list)

        CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
        save_path = os.path.join(CURRENT_DIR, 'htmls','test_data.js')
        comm.write_viewjs(view,save_path)
        self.ner_mklst_sender.emit(mark_list)
        self.finished.emit()


class ConnectThread(QThread):
    msg_sender = pyqtSignal(str)
    conn_sender = pyqtSignal(bool)
    def __init__(self,client,addr):
        super().__init__()
        self.client = client
        self.server_addr = addr

    def run(self):
        msg = f'[CONNECT - INFO - {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}' \
            f' - server_ip={self.server_addr[0]},server_port={self.server_addr[-1]}]: - '
        try:
            self.client.connect(self.server_addr)
            msg += f' Connect Successfully'
            self.conn_sender.emit(True)
        except Exception as e:
            print(e)
            msg += f' Connect Failed.The Reason:{e}'
            self.conn_sender.emit(False)
        self.msg_sender.emit(msg)


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.worker = None
        self.addr = ('127.0.0.1', 8888) # 默认的本地服务器地址
        self.initUI()
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connectServer(self.addr)
        QApplication.setStyle(QStyleFactory.keys()[2])


    def initUI(self):
        self.resize(1400,800)
        self.setWindowTitle('中医电子病历实体识别系统')

        self.tree_widget = TreeWidget()
        self.satck_widget = QStackedWidget()
        self.home_widget = HomeWidget()
        self.satck_widget.addWidget(self.home_widget)

        self.ner_widget = NerWidget()
        self.satck_widget.addWidget(self.ner_widget)

        self.mark_widget = MarkWidget()
        self.satck_widget.addWidget(self.mark_widget)

        self.data_center_widget = DataCenterWidget()
        self.satck_widget.addWidget(self.data_center_widget)

        self.setting_widget = SettingWidget()
        self.setting_widget.addr_sender.connect(self.connectServer)
        self.satck_widget.addWidget(self.setting_widget)

        self.about_widget = AboutWidget()
        self.satck_widget.addWidget(self.about_widget)
        self.satck_widget.setCurrentIndex(0)

        hlayout = QHBoxLayout()
        hlayout.addWidget(self.tree_widget)
        hlayout.addWidget(self.satck_widget)
        hlayout.setStretch(0,1)
        hlayout.setStretch(1,6)
        self.setLayout(hlayout)

        self.tree_widget.clicked.connect(self.onClickedTree)
        self.ner_widget.submit_signal.connect(self.handleNer)
        self.home_widget.user_button.clicked.connect(self.onClickedUserButton)

        self.setWindowIcon(QIcon(f'{CUR_PATH}/image/main-icon.png'))

    def onClickedTree(self, index):
        self.satck_widget.setCurrentIndex(index.row())

    def handleNer(self,src):
        # 这里发消息给server
        self.worker = WorkThread(src,self.client)
        self.worker.ner_mklst_sender.connect(self.ner_widget.set_ner_mark_list)
        self.worker.finished.connect(self.showRes)
        self.worker.start()



    def showRes(self):
        if self.worker:
            self.worker.quit()
        self.ner_widget.showNerRes()

    def connectServer(self,addr):
        '''
        :param addr: (ip,port)
        :return:
        '''
        # 这里处理逻辑需要改进，当已经和目标服务器连接上时，不需要重新建立连接。
        # 非目标服务器时，需要先断开和原来服务器的连接，然后重新建立和新服务器的连接
        self.client_thread = ConnectThread(self.client,addr)
        self.client_thread.msg_sender.connect(self.setting_widget.showConnectInfo)
        self.client_thread.conn_sender.connect(self.handleConnInfo)
        self.client_thread.start()

    def handleConnInfo(self,is_conn):
        self.ner_widget.setConnStatus(is_conn)
        if not is_conn:
            self.client_thread.quit()

    def onClickedUserButton(self):
        x = self.pos().x() + self.size().width() - self.home_widget.user_widget.width()
        y = self.pos().y() + 130
        self.home_widget.user_widget.move(x, y)
        # 这里使用exec_,使对话框变为模态对话框
        self.home_widget.user_widget.exec_()
        # self.home.user_widget.destroy()


    def closeEvent(self, QCloseEvent):
            self.client.close()
            print('clien close')


if __name__=='__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


