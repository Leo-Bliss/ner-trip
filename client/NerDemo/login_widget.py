#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@Time    :    2021/4/30 0030 5:56
#@Author  :    tb_youth
#@FileName:    login_widget.py
#@SoftWare:    PyCharm
#@Blog    :    https://blog.csdn.net/tb_youth





import sys
from PyQt5.QtWidgets import QApplication,QWidget,QLineEdit,QPushButton,QLabel,QCompleter,QMainWindow
from PyQt5.QtWidgets import QHBoxLayout,QVBoxLayout,QCheckBox,QAction,QToolBar,QMessageBox,QStyleFactory
from PyQt5.QtCore import Qt,pyqtSignal,QObject,QStringListModel
from PyQt5.QtGui import QFont
import base64
import os
import re

from PyQt5.QtGui import QIcon,QPainter,QPixmap

from NerDemo.localDB.src_ import DBOperator
from NerDemo.localDB.src_ import MD5
from NerDemo.utils import CommonHelper as comm

CUR_PATH = os.path.abspath(os.path.dirname(__file__))

class EmitUserInforSignal(QObject):
    sendmsg = pyqtSignal(tuple,tuple)

    def run(self,infor,icon_infor):
        print('start emit')
        self.sendmsg.emit(infor,icon_infor)


class LoginWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        QApplication.setStyle(QStyleFactory.keys()[2])

    def initUI(self):
        self.resize(533,408)
        self.setWindowTitle('中医电子病历实体识别系统')
        self.setProperty('name','UI')
        icon_path = os.path.join(CUR_PATH,'image','main-icon.png')
        self.setWindowIcon(QIcon(icon_path))
        self.setWindowFlags(Qt.WindowCloseButtonHint|Qt.WindowMinimizeButtonHint)
        self.send = EmitUserInforSignal()


        self.id_label = QLabel('账号')
        self.id_lineEdit = QLineEdit()
        hlayout1 = QHBoxLayout()
        hlayout1.addWidget(self.id_label)
        hlayout1.addWidget(self.id_lineEdit)

        self.password_label = QLabel('密码')
        self.password_lineEdit = QLineEdit()
        hlayout2 = QHBoxLayout()
        hlayout2.addWidget(self.password_label)
        hlayout2.addWidget(self.password_lineEdit)

        self.checkBox1 = QCheckBox('注册账号')
        self.checkBox2 = QCheckBox('记住密码')
        self.findPassword_action = QAction('找回密码')

        hlayout3 = QHBoxLayout()
        hlayout3.addWidget(self.checkBox1)
        hlayout3.addWidget(self.checkBox2)

        self.tool_bar = QToolBar()
        self.tool_bar.addAction(self.findPassword_action)
        hlayout3.addWidget(self.tool_bar)

        self.login_button = QPushButton('登录')
        self.login_button.setProperty('name','loginButton')
        qss_path = os.path.join(CUR_PATH,'qss','login.css')
        qssStyle = comm.readQSS(qss_path)
        self.setStyleSheet(qssStyle)

        #使用了qss时会无效
        # palette = QPalette()
        # pix = QPixmap(r'./image/home-center.jpg')
        # pix.scaled(self.width(),self.height())
        # palette.setBrush(QPalette.Background,QBrush(pix))
        # self.setPalette(palette)

        vlayout = QVBoxLayout()
        vlayout.addStretch(18)
        vlayout.addLayout(hlayout1,1)
        vlayout.addLayout(hlayout2,1)
        vlayout.addLayout(hlayout3,1)
        vlayout.addWidget(self.login_button,1)
        vlayout.addStretch(2)

        left_vlayout = QVBoxLayout()
        self.other_login = QPushButton('第三方登录')
        self.other_login.setFlat(True)
        left_vlayout.addStretch(1)
        left_vlayout.addWidget(self.other_login)

        right_vlayout = QVBoxLayout()
        self.tool_bar2 = QToolBar()
        self.QRC_action = QAction('二维码登录')
        self.tool_bar2.addAction(self.QRC_action)
        right_vlayout.addStretch(1)
        right_vlayout.addWidget(self.tool_bar2)
        icon_path = os.path.join(CUR_PATH,'image','二维码.png')
        icon = QIcon(icon_path)
        self.QRC_action.setIcon(icon)
        self.tool_bar2.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        self.first_psw = None
        self.second_psw = None
        self.id_lineEdit.setFont(QFont('宋体',25))
        self.password_lineEdit.setEchoMode(QLineEdit.Password)
        #设置清除按钮
        # self.id_lineEdit.setClearButtonEnabled(True)
        # self.password_lineEdit.setClearButtonEnabled(True)
        #设置自动补全列表
        user_list = self.loadLoaclUserList()
        self.completer = QCompleter()
        model = QStringListModel()
        model.setStringList(user_list)
        self.completer.setModel(model)
        self.id_lineEdit.setCompleter(self.completer)
        #密码长度
        self.password_lineEdit.setMaxLength(16)

        self.id_label.setToolTip('建议您使用邮箱注册')
        self.password_label.setToolTip('密码最大长度为16')
        self.id_lineEdit.setText("admin@qq.com")
        self.password_lineEdit.setText("123456")

        hlayout = QHBoxLayout()
        hlayout.addLayout(left_vlayout,1)
        hlayout.addLayout(vlayout,2)
        hlayout.addLayout(right_vlayout,1)
        self.setLayout(hlayout)

        self.checkBox1.stateChanged.connect(self.checkStatus)
        self.login_button.clicked.connect(self.onClickLogin)




    #背景图片铺满窗口
    def paintEvent(self,event):
        painter = QPainter(self)
        bk_path = os.path.join(CUR_PATH,'image','login.jpg')
        painter.drawPixmap(0,0,self.width(),self.height(),QPixmap(bk_path))

    def onClickLogin(self):
        if self.checkBox1.isChecked():
            print('注册')
            self.registeUser()
        else:
            print('登录')
            db = os.path.join(CUR_PATH,'localDB','db','userDB.db')
            operator = DBOperator.DBOperator(db)
            id = self.id_lineEdit.text()
            psw = self.password_lineEdit.text()
            sql = "select * from user where user_id='{}'".format(id)
            try:
                res = operator.query(sql)
                # print(res)
                if not len(res):
                    QMessageBox.information(self, '关于', '该用户不存在！', QMessageBox.Ok)
                    return
                else:
                    res = res[0]
                    md5 = MD5.MD5()
                    if md5.md5Encode(psw) != res[2]:
                        QMessageBox.information(self, '结果', '密码错误')
                        return
                    else:
                        print('登录成功！')
                        self.addLocalUser(id)
                        sql = "select * from user_icon where user_id='{}'".format(id)
                        icon_infor = operator.query(sql)[0]
                        self.saveUserIcon(icon_infor)
                        # print(icon_infor)
                        self.send.run(res,icon_infor)
                        self.close()
            except Exception as e:
                print(e)

    def registeUser(self):
        # #账号合法性检查
        # self.id_lineEdit.setPlaceholderText('请输入邮箱')
        user_id = self.id_lineEdit.text()
        # pattern = '\w+@\w+.com'
        # res_match = re.search(pattern, user_id)
        db = os.path.join(CUR_PATH,'localDB','db','userDB.db')
        operator = DBOperator.DBOperator(db)
        sql = "select * from user where user_id='{}'".format(user_id)
        res = operator.query(sql)
        print(res)
        if len(res):
            QMessageBox.information(self, '关于', '该用户已经存在,建议您使用邮箱注册！', QMessageBox.Ok)
        else:
            self.second_psw = self.password_lineEdit.text()
            if self.second_psw!=self.first_psw:
                QMessageBox.information(self, '关于', '前后输入密码不一致！', QMessageBox.Ok)
            else:
                md5 = MD5.MD5()
                sql = 'select * from user'
                res = operator.query(sql)
                user_dict = {
                    'user_id': user_id,
                    'user_name': 'user{}'.format(len(res)),
                    'password': md5.md5Encode(self.second_psw),
                    'personal_tables': '',
                    'icon_path': os.path.join(CUR_PATH,'userIcon','user01.png')
                }
                operator.addUser(user_dict)
                QMessageBox.about(QMainWindow(),'关于','注册成功!')



    def checkStatus(self,cb):
        if self.checkBox1.isChecked():
            self.login_button.setText('注册')
            # 再次输入密码
            self.first_psw = self.password_lineEdit.text()
            self.password_lineEdit.clear()
            self.password_lineEdit.setPlaceholderText('再次输入确认密码')
            self.password_lineEdit.setFocus()
        else:
            self.password_lineEdit.setPlaceholderText('')
            self.login_button.setText('登录')

    def saveUserIcon(self,icon_infor):
        file_name = "{}/userIcon/{}#{}.{}".format(CUR_PATH,icon_infor[0], icon_infor[1], icon_infor[2])
        if os.path.exists(file_name):
            return
        with open(file_name, "wb") as f:
            f.write(base64.b64decode(icon_infor[-1]))

    #加载本地用户列表
    def loadLoaclUserList(self):
        with open(f'{CUR_PATH}/localUser/local.txt','r',encoding='utf-8') as f:
            data = f.read()
            users = data.split(',')
            # print(users)
            return users[:-1]

    #添加到本地用户列表
    def addLocalUser(self,user_id):
        if user_id not in self.loadLoaclUserList():
            with open(f'{CUR_PATH}/localUser/local.txt','a',encoding='utf-8') as f:
                f.write(user_id+',')




if __name__=='__main__':
    app = QApplication(sys.argv)
    window = LoginWidget()
    window.show()
    sys.exit(app.exec_())
