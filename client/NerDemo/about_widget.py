#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@Time    :    2021/4/28 0028 1:38
#@Author  :    tb_youth
#@FileName:    about_widget.py
#@SoftWare:    PyCharm
#@Blog    :    https://blog.csdn.net/tb_youth


'''
显示本项目的一些信息,
跳转到github/gitee仓库。
'''
import sys
import os.path

import webbrowser
from PyQt5.QtWidgets import QApplication,QWidget
from PyQt5.QtWidgets import QVBoxLayout,QPushButton
from PyQt5.QtGui import QIcon
from NerDemo.utils import CommonHelper as common


from PyQt5.QtCore import pyqtProperty, pyqtSignal, QObject, QTextCodec, QUrl
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWebEngineWidgets import QWebEngineView

CUR_PATH = os.path.dirname(os.path.realpath(__file__))


class Document(QObject):
    textChanged = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.m_text = ""

    def get_text(self):
        return self.m_text

    def set_text(self, text):
        if self.m_text == text:
            return
        self.m_text = text
        self.textChanged.emit(self.m_text)

    text = pyqtProperty(str, fget=get_text, fset=set_text, notify=textChanged)


class DownloadManager(QObject):
    finished = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self._manager = QNetworkAccessManager()
        self.manager.finished.connect(self.handle_finished)

    @property
    def manager(self):
        return self._manager

    def start_download(self, url):
        self.manager.get(QNetworkRequest(url))

    def handle_finished(self, reply):
        if reply.error() != QNetworkReply.NoError:
            print("error: ", reply.errorString())
            return
        codec = QTextCodec.codecForName("UTF-8")
        raw_data = codec.toUnicode(reply.readAll())
        self.finished.emit(raw_data)



class AboutWidget(QWidget):
    def __init__(self):
        super(AboutWidget,self).__init__()
        self.initUI()

    def initUI(self):
        self.resize(800,800)

        file_name = os.path.join(CUR_PATH, r"htmls\mkdown\index.html")


        self.document = Document()
        self.download_manager = DownloadManager()

        self.channel = QWebChannel()
        self.channel.registerObject("content", self.document)

        # remote or local markdown file
        root_path = CUR_PATH.rsplit('\\',maxsplit=2)[0]
        url = os.path.join(root_path,"README.md")
        markdown_url = QUrl.fromUserInput(
           url
        )
        self.download_manager.finished.connect(self.document.set_text)
        self.download_manager.start_download(markdown_url)

        self.view = QWebEngineView()
        self.view.page().setWebChannel(self.channel)
        url = QUrl.fromLocalFile(file_name)
        self.view.load(url)


        self.button = QPushButton('去Star本项目')
        self.button.setIcon(QIcon(f'{CUR_PATH}/image/star.png'))
        qss_file = f'{CUR_PATH}/qss/about.css'
        style = common.readQSS(qss_file)
        self.button.setStyleSheet(style)
        vlayout = QVBoxLayout()
        vlayout.addWidget(self.view)
        vlayout.addWidget(self.button)
        self.setLayout(vlayout)
        self.button.clicked.connect(self.onClickedOpen)


    def onClickedOpen(self):
        url = r'https://gitee.com/tbyouth/ner'
        webbrowser.open(url)





if __name__=='__main__':
    app = QApplication(sys.argv)
    window = AboutWidget()
    window.show()
    sys.exit(app.exec_())

