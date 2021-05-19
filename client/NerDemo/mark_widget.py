#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@Time    :    2021/4/25 0025 10:59
#@Author  :    tb_youth
#@FileName:    mark_widget.py
#@SoftWare:    PyCharm
#@Blog    :    https://blog.csdn.net/tb_youth
import sys
import os
import json
from PyQt5.QtCore import QDir,Qt

from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QVBoxLayout, QFileDialog, QSplitter, \
    QStatusBar

from PyQt5.QtWidgets import QHBoxLayout

from NerDemo.base_widgets import TableView,GroupBox
from NerDemo.utils import  LoadToTableThread, WriteExcelThread
from NerDemo.utils import CommonHelper as common

CUR_PATH = os.path.abspath(os.path.dirname(__file__))

class MarkWidget(QWidget):
    def __init__(self):
        super(MarkWidget,self).__init__()
        self.load_thread = None
        self.initUI()

    def getEntitySetting(self):
        setting_path = os.path.join(CUR_PATH, 'setting', 'entity.json')
        with open(setting_path, mode='r', encoding='utf-8') as f:
            txt = f.read()
        mp = json.loads(txt)
        return mp

    def initUI(self):
        self.resize(1200,750)
        self.input_line = QLineEdit()
        self.input_line.setPlaceholderText('文件路径')
        self.input_button = QPushButton('导入')
        hlayout = QHBoxLayout()
        hlayout.addWidget(self.input_line)
        hlayout.addWidget(self.input_button)
        self.tableview = TableView()
        mp = self.getEntitySetting()
        color = mp['entity-color']
        nk_entity = mp['nickname-entity']
        entity_list = [[v,color[k]] for k,v in nk_entity.items()]
        self.label_group = GroupBox(entity_list)
        hsplitter = QSplitter(Qt.Horizontal)
        hsplitter.addWidget(self.tableview)
        hsplitter.addWidget(self.label_group)
        hsplitter.setSizes([950, 50])
        hlayout2 = QHBoxLayout()
        hlayout2.addWidget(hsplitter)

        hlayout3 = QHBoxLayout()
        self.status_bar = QStatusBar()
        self.save_button = QPushButton('暂存标注')
        self.output_button = QPushButton('导出标注')
        hlayout3.addWidget(self.status_bar)
        hlayout3.addStretch(0)
        hlayout3.addWidget(self.save_button)
        hlayout3.addWidget(self.output_button)

        vlayout = QVBoxLayout()
        vlayout.addLayout(hlayout)
        vlayout.addLayout(hlayout2)
        vlayout.addLayout(hlayout3)
        self.setLayout(vlayout)

        self.input_button.clicked.connect(self.loadFile)
        self.output_button.clicked.connect(self.outputMarkList)
        self.save_button.clicked.connect(self.saveMarkData)



    def loadFile(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setFilter(QDir.Files)
        if dialog.exec_():
            file_name = dialog.selectedFiles()[0]
            self.input_line.setText(file_name)
            self.load_thread = LoadToTableThread(file_name)
            self.load_thread.finished_signal.connect(self.tableview.loadData)
            self.load_thread.end_signal.connect(self.load_thread.quit)
            self.load_thread.start()


    def showStatus(self,msg):
        self.status_bar.showMessage(msg,2000)

    def outputMarkList(self):
        file_path, _ = QFileDialog.getSaveFileName(self, '保存文件', '', 'AnyFile(*.*);;csv(*.csv);;xlsx(*.xlsx);;xls(*.xls)')
        if file_path is None:
            return
        mark_data = self.tableview.getMarkData()
        if mark_data is None:
            return
        mark_list = common.get_mark_list(mark_data)
        header = ['entity_class','start_pos','end_pos','content']
        self.write_excel_thread = WriteExcelThread(mark_list,cols=header,save_path=file_path)
        self.write_excel_thread.signal.connect(self.showStatus)
        self.write_excel_thread.signal.connect(self.write_excel_thread.quit)
        self.write_excel_thread.start()


    def saveMarkData(self):
        file_path, _ = QFileDialog.getSaveFileName(self, '保存文件', '','AnyFile(*.*);;csv(*.csv);;xlsx(*.xlsx);;xls(*.xls)')
        if file_path is None:
            return
        mark_data = self.tableview.getMarkData()
        print(mark_data)














if __name__=='__main__':
    app = QApplication(sys.argv)
    window = MarkWidget()
    window.show()
    sys.exit(app.exec_())


