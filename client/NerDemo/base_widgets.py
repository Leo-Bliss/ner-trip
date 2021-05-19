#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@Time    :    2021/4/26 0026 3:35
#@Author  :    tb_youth
#@FileName:    base_widgets.py
#@SoftWare:    PyCharm
#@Blog    :    https://blog.csdn.net/tb_youth


from PyQt5.QtGui import QStandardItemModel,QCursor
from PyQt5.QtWidgets import  QTableView, QVBoxLayout, QApplication, QAbstractItemView,QGroupBox, QLabel,  QMenu

import sys
import os
import json

from PyQt5.QtCore import QSize, pyqtProperty, QTimer, Qt
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtWidgets import QWidget



from NerDemo.utils import CommonHelper as common

CUR_PATH = os.path.abspath(os.path.dirname(__file__))

class TableView(QWidget):
    def __init__(self):
        super(TableView,self).__init__()
        self.initUI()

    def getEntitySetting(self):

        setting_path = os.path.join(CUR_PATH, 'setting', 'entity.json')
        with open(setting_path, mode='r', encoding='utf-8') as f:
            txt = f.read()
        mp = json.loads(txt)
        return mp


    def initUI(self):
        self.resize(800, 400)
        self.model = QStandardItemModel(15, 100)
        self.char_indexs = []
        self.mark_data = None
        self.entity_mp = self.getEntitySetting()
        self.tableview = QTableView()
        # 关联model
        self.tableview.setModel(self.model)
        self.tableview.setFocusPolicy(Qt.NoFocus)  # 隐藏选中时的虚线框
        self.tableview.setShowGrid(False)  # 表格边框
        qss = common.readQSS(f'{CUR_PATH}/qss/table.css')

        self.tableview.setStyleSheet(qss)
        self.tableview.resizeColumnsToContents()
        self.tableview.resizeRowsToContents()

        # frame
        # self.tableview.setFrameShape(QFrame.NoFrame)
        # header
        self.tableview.horizontalHeader().setVisible(False)
        #  右键菜单栏
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.contextMenu = QMenu()
        self.mark_menu = QMenu('标注')
        self.initMarkMenu()
        self.contextMenu.addMenu(self.mark_menu)
        self.removeMarkAction = self.contextMenu.addAction('撤销')
        self.removeMarkAction.triggered.connect(self.removeMark)
        # self.viewMarkAction = self.contextMenu.addAction('查看')
        self.customContextMenuRequested.connect(self.rightMenuShow)
        # 不可编辑
        self.tableview.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 布局
        layout = QVBoxLayout()
        layout.addWidget(self.tableview)
        self.setLayout(layout)

    def initMarkMenu(self):
        entity_list = self.entity_mp['nickname-entity'].values()
        for entity in entity_list:
            action = self.mark_menu.addAction(entity)
            action.setObjectName(entity)
            action.triggered.connect(self.mark)

    def loadData(self,md,mk,cd):
        self.model = md
        self.mark_data = mk
        self.char_indexs = cd
        self.tableview.setModel(self.model)
        # 单元格内容自适应在加载数据后还需要调用一下
        self.tableview.resizeColumnsToContents()
        self.tableview.resizeRowsToContents()

    def mark(self):
        '''
        采用基于字的BIO
        :return:
        '''
        entity = self.sender().objectName()
        select_indexs = self.tableview.selectedIndexes()
        color = self.entity_mp['entity-color']
        nk_entity = self.entity_mp['nickname-entity']
        entity_nk = self.entity_mp['entity-nickname']
        entity_color_dict = {v: color[k] for k, v in nk_entity.items()}
        for i,index in enumerate(select_indexs):
            item = self.model.item(index.row(),index.column())
            if item is None:
                continue
            x,y = index.row(),index.column()
            print(self.char_indexs[x][y])
            if i == 0:
                self.mark_data[self.char_indexs[x][y]][-1] = 'B-' + entity_nk[entity]
            else:
                self.mark_data[self.char_indexs[x][y]][-1] = 'I-' + entity_nk[entity]
            # item.setBackground(QColor(entity_color_dict[entity])) # why it not work?
            item.setForeground(QColor(entity_color_dict[entity]))


    def removeMark(self):
        select_indexs = self.tableview.selectedIndexes()
        for index in select_indexs:
            item = self.model.item(index.row(), index.column())
            if item is None:
                continue
            x, y = index.row(), index.column()
            print(self.char_indexs[x][y])
            self.mark_data[self.char_indexs[x][y]][-1] = 'O'
            # 恢复未标记的颜色
            item.setForeground(QColor('black'))

    def getMarkData(self):
        return self.mark_data

    def rightMenuShow(self):
        self.contextMenu.popup(QCursor.pos())
        self.contextMenu.show()



class Label(QWidget):
    def __init__(self,name,color='red'):
        super(Label,self).__init__()
        self.initUI(name,color)

    def initUI(self,name,color):
        self.name_label = QLabel(name)
        self.color_label = QLabel()
        # self.color_label.setMinimumSize(35,8)
        self.color_label.setMaximumSize(75,15)
        self.setColor(color)
        layout = QVBoxLayout()
        layout.addWidget(self.name_label)
        layout.addWidget(self.color_label)
        layout.setStretch(0,2)
        layout.setStretch(1,1)
        layout.setSpacing(2)
        self.setLayout(layout)


    def setColor(self,color):
        color_style = f'background-color:{color};border-radius:2px;'
        # print(color_style)
        self.color_label.setStyleSheet(color_style)



class GroupBox(QGroupBox):
    def __init__(self,entity_labels):
        super(GroupBox, self).__init__()
        self.initUI(entity_labels)

    def initUI(self,entity_labels):
        self.setTitle('标签')
        vlayout = QVBoxLayout()
        if entity_labels:
            for entity,color in entity_labels:
                self.entity_label = Label(name=entity,color=color)
                vlayout.addWidget(self.entity_label)
            vlayout.setSpacing(0)
            vlayout.addStretch(10)


        self.setLayout(vlayout)




'''
进度条
'''

class CircleProgressBar(QWidget):
    # 圆圈颜色
    Color = QColor(24, 189, 155)
    # 顺时针
    Clockwise = True
    # 角度步长，可以调节转速
    Delta = 36

    def __init__(self, *args, color=None, clockwise=True, **kwargs):
        super(CircleProgressBar, self).__init__(*args, **kwargs)
        self.setFixedSize(30,30)
        self.angle = 0
        self.Clockwise = clockwise
        if color:
            self.Color = color
        '''
        实例化Qtimer，连接timeout()信号到适当的槽函数，并调用start()，
        然后在恒定的时间间隔会发射timeout()信号。
        '''
        self._timer = QTimer(self, timeout=self.update)
        self._timer.start(100)

    def paintEvent(self, event):
        super(CircleProgressBar, self).paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)
        side = min(self.width(), self.height())
        painter.scale(side / 100.0, side / 100.0)
        painter.rotate(self.angle)
        painter.save()
        painter.setPen(Qt.NoPen)
        color = self.Color.toRgb()
        for i in range(11):
            color.setAlphaF(1.0 * i / 10)
            painter.setBrush(color)
            painter.drawEllipse(30, -10, 20, 20)
            painter.rotate(36)
        painter.restore()
        self.angle += self.Delta if self.Clockwise else -self.Delta
        self.angle %= 360

    @pyqtProperty(QColor)
    def color(self) -> QColor:
        return self.Color

    @color.setter
    def color(self, color: QColor):
        if self.Color != color:
            self.Color = color
            self.update()

    @pyqtProperty(bool)
    def clockwise(self) -> bool:
        return self.Clockwise

    @clockwise.setter
    def clockwise(self, clockwise: bool):
        if self.Clockwise != clockwise:
            self.Clockwise = clockwise
            self.update()

    @pyqtProperty(int)
    def delta(self) -> int:
        return self.Delta

    @delta.setter
    def delta(self, delta: int):
        if self.delta != delta:
            self.delta = delta
            self.update()

    def sizeHint(self) -> QSize:
        return QSize(100, 100)




if __name__ == '__main__':
    pass
    app = QApplication(sys.argv)
    window = TableView()
    window.show()
    sys.exit(app.exec_())