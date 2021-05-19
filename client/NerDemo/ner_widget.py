#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@Time    :    2021/4/26 0026 3:28
#@Author  :    tb_youth
#@FileName:    ner_widget.py
#@SoftWare:    PyCharm
#@Blog    :    https://blog.csdn.net/tb_youth

import sys
import os

from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QWidget, QTextEdit, QPushButton, QHBoxLayout, QVBoxLayout, QApplication, QFrame, \
    QSplitter, QFileDialog, QStatusBar, QMessageBox
from PyQt5.QtCore import Qt, QDir, pyqtSignal, QUrl

from NerDemo.base_widgets import CircleProgressBar
from NerDemo.utils import ReadFileThread, WriteExcelThread

CUR_PATH = os.path.abspath(os.path.dirname(__file__))

class NerWidget(QWidget):
    submit_signal =  pyqtSignal(str)
    def __init__(self):
        super(NerWidget,self).__init__()
        self.initUI()
        self.__is_conn = False
        self.nermklst = []

    def initUI(self):
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText('电子病历内容')
        self.input_button = QPushButton('导入')
        self.submit_button = QPushButton('提交')

        hlayout = QHBoxLayout()
        hlayout.addStretch(0)
        hlayout.addWidget(self.input_button)
        hlayout.addWidget(self.submit_button)

        vlayout = QVBoxLayout()
        vlayout.addWidget(self.text_edit)
        vlayout.addLayout(hlayout)

        self.top = QFrame()
        self.top.setLayout(vlayout)

        self.browser = QWebEngineView()

        self.bottom = QFrame()
        hlayout1 = QHBoxLayout()
        hlayout1.addWidget(self.browser)

        self.bottom.setLayout(hlayout1)

        vsplitter = QSplitter(Qt.Vertical)
        vsplitter.addWidget(self.top)
        vsplitter.addWidget(self.bottom)
        vsplitter.setSizes([200, 800])

        layout = QVBoxLayout()
        layout.addWidget(vsplitter)
        hlayout2 = QHBoxLayout()
        self.progressbar = CircleProgressBar()
        self.progressbar.hide()
        self.reload_button = QPushButton('刷新')
        self.output_button = QPushButton('导出')
        hlayout2.addWidget(self.progressbar)
        self.status_bar = QStatusBar()
        hlayout2.addWidget(self.status_bar)
        hlayout2.addStretch(0)
        hlayout2.addWidget(self.reload_button)
        hlayout2.addWidget(self.output_button)
        self.footer = QFrame()
        self.footer.setLayout(hlayout2)
        layout.addWidget(self.footer)
        self.setLayout(layout)
        self.input_button.clicked.connect(self.onClickInputBtn)
        self.submit_button.clicked.connect(self.onClickedSubmitBtn)
        self.reload_button.clicked.connect(self.showNerRes)
        self.output_button.clicked.connect(self.onClickedOutputBtn)


    def showData(self,data):
        self.text_edit.setText(data)
        self.status_bar.showMessage('导入完成',2000)

    def showStatus(self,msg):
        self.status_bar.showMessage(msg,2000)

    def onClickInputBtn(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setFilter(QDir.Files)
        if dialog.exec_():
            file_name = dialog.selectedFiles()[0]
            self.text_edit.setText(file_name)
            self.status_bar.showMessage('导入文件中...')
            self.file_open_thread = ReadFileThread(file_name)
            self.file_open_thread.finished_signal.connect(self.showData)
            self.file_open_thread.finished_signal.connect(self.file_open_thread.quit)
            self.file_open_thread.start()


    def onClickedSubmitBtn(self):
        if self.__is_conn:
            data = self.text_edit.toPlainText()
            if len(data) == 0:
                QMessageBox.information(self, '无内容', '请输入/导入识别文本', QMessageBox.Yes, QMessageBox.Yes)
                return
            self.submit_button.setEnabled(False)
            self.progressbar.show()
            self.status_bar.showMessage('实体识别中,请耐心等待...')
            self.submit_signal.emit(data)
        else:
            QMessageBox.critical(self,'错误','你的服务器走丢了哦，请在系统设置中检查服务器设置。',QMessageBox.Yes,QMessageBox.Yes)

    def onClickedOutputBtn(self):
        file_path, _ = QFileDialog.getSaveFileName(self, '保存文件', '','AnyFile(*.*);;csv(*.csv);;xlsx(*.xlsx);;xls(*.xls)')
        if file_path is None:
            return
        if self.ner_mklst:
            header = ['entity_class', 'start_pos', 'end_pos', 'content']
            self.write_excel_thread = WriteExcelThread(self.ner_mklst, cols=header, save_path=file_path)
            self.write_excel_thread.signal.connect(self.showStatus)
            self.write_excel_thread.signal.connect(self.write_excel_thread.quit)
            self.write_excel_thread.start()

    def set_ner_mark_list(self,lst):
        self.ner_mklst = lst

    def showNerRes(self):
        print('='*100)
        # url = r'D:\NER\client\NerDemo\htmls\ner_view.html'
        url = os.path.join(CUR_PATH,'htmls','ner_view.html')
        self.browser.load(QUrl.fromLocalFile(url))
        self.submit_button.setEnabled(True)
        self.progressbar.close()
        self.status_bar.showMessage('实体识别完成！',5000)

    def setConnStatus(self,status):
        '''
        :param status: bool
        :return:
        '''
        self.__is_conn = status








if __name__=='__main__':
    app = QApplication(sys.argv)
    window = NerWidget()
    window.show()
    sys.exit(app.exec_())
