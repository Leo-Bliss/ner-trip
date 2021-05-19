#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@Time    :    2021/4/30 0030 5:48
#@Author  :    tb_youth
#@FileName:    home_widget.py
#@SoftWare:    PyCharm
#@Blog    :    https://blog.csdn.net/tb_youth


import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout, QMenu, QDialog
from PyQt5.QtWidgets import QAction, QLineEdit, QToolBar, QVBoxLayout, QPushButton
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt

from NerDemo.utils import CommonHelper as comm
from NerDemo.login_widget import LoginWidget

CUR_PATH = os.path.abspath(os.path.dirname(__file__))

class User():
    def __init__(self, id='admin01@qq.com', name='visitor', icon=f'{CUR_PATH}/userIcon/user01.png'):
        self.id = id
        self.name = name
        self.icon = icon


class UserInfor(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(300, 500)
        icon_path= os.path.join(CUR_PATH,'image','user01.png')
        self.setWindowIcon(QIcon(icon_path))
        self.setWindowTitle('User')
        self.personButton = QPushButton('个人中心')
        self.messageButton = QPushButton('我的通知')
        self.accountButton = QPushButton('登录账号')
        self.logoutButton = QPushButton('退出登录')

        layout = QVBoxLayout()
        layout.addWidget(self.personButton)
        layout.addWidget(self.messageButton)
        layout.addWidget(self.accountButton)
        layout.addWidget(self.logoutButton)
        layout.setSpacing(15)
        layout.addStretch(1)
        self.setLayout(layout)


class HomeWidget(QWidget):
    def __init__(self):
        super(HomeWidget, self).__init__()
        self.initUI()

    def initUI(self):
        self.resize(1000, 800)
        self.user_widget = UserInfor()
        self.loginWindow = LoginWidget()

        self.label = QLabel("导航")
        hlayout1 = QHBoxLayout()
        hlayout2 = QHBoxLayout()
        hlayout1.addWidget(self.label)
        hlayout1.addLayout(hlayout2)
        hlayout1.setStretch(0, 1)
        hlayout1.setStretch(1, 14)
        self.line_edit = QLineEdit()
        hlayout2.addWidget(self.line_edit)
        self.visit_data = QAction("访问数据")
        self.analysis_data = QAction("分析数据")
        self.upload_data = QAction("上传数据")
        self.manage_setting = QAction("管理设置")
        # self.user_center = QAction('用户中心')
        self.tool_bar = QToolBar()
        self.tool_bar.addAction(self.visit_data)
        self.tool_bar.addSeparator()
        self.tool_bar.addAction(self.analysis_data)
        self.tool_bar.addSeparator()
        self.tool_bar.addAction(self.upload_data)
        self.tool_bar.addSeparator()
        self.tool_bar.addAction(self.manage_setting)
        self.tool_bar.addSeparator()
        # self.tool_bar.addAction(self.user_center)
        self.tool_bar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.user_button = QPushButton("admin")

        hlayout2.addWidget(self.tool_bar)
        hlayout2.addWidget(self.user_button)

        # 显示用户信息
        qss_path = os.path.join(CUR_PATH,'qss','user.css')
        qssStyle = comm.readQSS((qss_path))
        self.user_button.setStyleSheet(qssStyle)
        self.now_user = User()
        self.loadUser(self.now_user)
        self.userPos = self.user_button.pos()

        # 首页中心图片
        self.label = QLabel()
        bk_path = os.path.join(CUR_PATH,'image','home-center.jpg')
        self.label.setPixmap(QPixmap(bk_path))

        # icon
        icon = QIcon()
        icon.addPixmap(QPixmap(f'{CUR_PATH}/image/访问数据.png'), QIcon.Normal, QIcon.Off)
        self.visit_data.setIcon(icon)
        icon = QIcon()
        icon.addPixmap(QPixmap(f'{CUR_PATH}/image/分析数据.png'), QIcon.Normal, QIcon.Off)
        self.analysis_data.setIcon(icon)
        icon = QIcon()
        icon.addPixmap(QPixmap(f'{CUR_PATH}/image/上传数据.png'), QIcon.Normal, QIcon.Off)
        self.upload_data.setIcon(icon)
        icon = QIcon()
        icon.addPixmap(QPixmap(f'{CUR_PATH}/image/管理设置.png'), QIcon.Normal, QIcon.Off)
        self.manage_setting.setIcon(icon)

        # 布局
        layout = QVBoxLayout()
        layout.addLayout(hlayout1)
        layout.addWidget(self.label)
        layout.setStretch(0, 1)
        layout.setStretch(1, 20)
        self.setLayout(layout)

        # self.user_button.clicked.connect(self.onClicked)
        self.user_widget.accountButton.clicked.connect(self.onClickAccountButton)
        self.user_widget.logoutButton.clicked.connect(self.onClickLogoutButton)
        self.loginWindow.send.sendmsg.connect(self.getUserInfor)

    def loadUser(self, user):
        self.user_button.setText(user.name)
        self.user_button.setIcon(QIcon(user.icon))
        # icon = QIcon()
        # icon.addPixmap(QPixmap(user_icon), QIcon.Normal, QIcon.Off)
        # self.user_center.setIcon(icon)
        # self.user_center.setText(user_name)
        self.user_widget.setWindowIcon(QIcon(user.icon))
        self.user_widget.setWindowTitle(user.name)

    def onClicked(self):
        print(233)
        x = self.pos().x() + self.size().width() - self.user_widget.width()
        y = self.pos().y() + 130
        self.user_widget.move(x, y)
        # 这里使用show,用于调试
        self.user_widget.show()

    def onClickAccountButton(self):
        self.loginWindow.setWindowModality(Qt.ApplicationModal)
        # x = self.pos().x() - self.loginWindow.width()
        # y = self.pos().y() + (self.height()-self.loginWindow.height())
        # self.loginWindow.move(x,y)
        self.user_widget.close()
        self.loginWindow.show()

    def getUserInfor(self, infor, icon_infor):
        file_name = r"{}/userIcon/{}#{}.{}".format(CUR_PATH,icon_infor[0], icon_infor[1], icon_infor[2])
        # print(file_name)
        # print('get：',infor)
        self.now_user = User(infor[0], infor[1], file_name)
        icon = QIcon(self.now_user.icon)
        self.user_widget.setWindowIcon(icon)
        self.user_button.setIcon(icon)
        self.user_widget.setWindowTitle(self.now_user.name)
        self.user_button.setText(self.now_user.name)
        self.user_widget.accountButton.setEnabled(False)

    def onClickLogoutButton(self):
        self.user_widget.accountButton.setEnabled(True)
        default = User()
        self.user_widget.setWindowTitle(default.name)
        self.user_widget.setWindowIcon(QIcon(default.icon))
        self.user_button.setText(default.name)
        self.user_button.setIcon(QIcon(default.icon))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = HomeWidget()
    window.show()
    sys.exit(app.exec_())
