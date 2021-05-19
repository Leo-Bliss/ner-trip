#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@Time    :    2021/4/23 0023 0:22
#@Author  :    tb_youth
#@FileName:    tree_widget.py
#@SoftWare:    PyCharm
#@Blog    :    https://blog.csdn.net/tb_youth


import sys
from PyQt5.QtWidgets import QApplication,QTreeWidget,QTreeWidgetItem
from PyQt5.QtGui import QIcon
import os

CUR_PATH = os.path.abspath(os.path.dirname(__file__))

class TreeWidget(QTreeWidget):
    def __init__(self):
        super(TreeWidget,self).__init__()
        self.initUI()

    def initUI(self):
        self.resize(800,800)
        self.setWindowTitle('TreeWidget')
        qss = '''
        QTreeWidget::item{height:36px;}
        '''
        self.setStyleSheet(qss)



        self.setColumnCount(1)
        # self.setHeaderLabels(['key'])
        self.header().hide()
        # 装饰根结点的三角形
        self.setRootIsDecorated(True)

        # self.setFocusPolicy(Qt.NoFocus) #item选中时的虚线框
        root0 = QTreeWidgetItem(self)
        root0.setText(0, '系统首页')
        root0.setIcon(0, QIcon(f'{CUR_PATH}/image/home.png'))
        self.setCurrentItem(root0)


        root1 = QTreeWidgetItem(self)
        root1.setText(0,'实体识别')
        root1.setIcon(0,QIcon(f'{CUR_PATH}/image/course.png'))


        root2 = QTreeWidgetItem(self)
        root2.setText(0,'标注工具')
        root2.setIcon(0,QIcon(f'{CUR_PATH}/image/address'))

        root3 = QTreeWidgetItem(self)
        root3.setText(0, '数据中心')
        root3.setIcon(0, QIcon(f'{CUR_PATH}/image/camera.png'))

        root4 = QTreeWidgetItem(self)
        root4.setText(0, '系统设置')
        root4.setIcon(0, QIcon(f'{CUR_PATH}/image/child'))

        root5 = QTreeWidgetItem(self)
        root5.setText(0, '关于我们')
        root5.setIcon(0, QIcon(f'{CUR_PATH}/image/favoriteslist.png'))



if __name__=='__main__':
    app = QApplication(sys.argv)
    window = TreeWidget()
    window.show()
    sys.exit(app.exec_())
