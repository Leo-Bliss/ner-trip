#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@Time    :    2020/1/5 0005 7:55
#@Author  :    tb_youth
#@FileName:    DBOperator.py
#@SoftWare:    PyCharm
#@Blog    :    https://blog.csdn.net/tb_youth

'''
对本地数据库进行操作：
1.创建数据库
2.数据增删查改
'''

from PyQt5.QtSql import QSqlDatabase
import sqlite3
import base64
from NerDemo.localDB.src_ import MD5

class DBOperator():
    def __init__(self,db_name):
        self.db_name = db_name

    def createDB(self):
        try:
            db = QSqlDatabase.addDatabase('QSQLITE')
            # 指定本地SQLite数据库名称
            db.setDatabaseName(self.db_name)
            if not db.open():
                print('无法建立与数据库的连接')
            db.close()
        except Exception as e:
            print(e)


    def update(self,sql, *args):
        conn = sqlite3.connect(self.db_name, detect_types=sqlite3.PARSE_DECLTYPES)
        cursor = conn.cursor()
        try:
            cursor.execute(sql, *args)
        except Exception as e:
            print(e)
            pass
        conn.commit()
        conn.close()

    def query(self,sql):
        conn = sqlite3.connect(self.db_name, detect_types=sqlite3.PARSE_DECLTYPES)
        cursor = conn.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        # print(data)
        conn.close()
        return data

    # 查看数据库中表的字段
    def showField(self,table_name):
        sql = "PRAGMA table_info({})".format(table_name)
        res = self.query(sql)
        return res

    def showTable(self,table_name):
        filed = self.showField(table_name)
        print(filed)
        sql = 'select * from {}'.format(table_name)
        res = self.query(sql)
        print('{}表共有{}条记录'.format(table_name,len(res)))
        for item in res:
            print(item)

    def addUser(self,dct):
        path = dct.get('icon_path')
        try:
            with open("{}".format(path), "rb") as f:
                content = base64.b64encode(f.read())
                dir, file = path.rsplit('/', maxsplit=1)
                file_name, file_type = file.rsplit('.', maxsplit=1)
                print(file_name, file_type)
        except Exception as e:
            print(e)
            return
        user_id = dct.get('user_id')

        #用户基本信息
        sql = 'insert into user values(?,?,?,?)'
        para = (user_id,dct.get('user_name'),dct.get('password'),dct.get('personal_tables'))
        self.update(sql,para)
        sql = 'select * from user'
        self.query(sql)

        #用户icon信息
        sql = "insert into user_icon values(?,?,?,?)"
        para = (user_id,file_name,file_type,content)
        self.update(sql,para)
        sql = 'select * from user_icon'
        self.query(sql)





if __name__ == '__main__':
    db_name = '../db/userDB.db'
    operator = DBOperator(db_name)
    #创建用户数据库
    #operator.createDB()

    #暂时只做一个简单的登入系统

    # #建立用户表,#将user_id账号注时设置为以邮箱注册
    # sql = 'create table user(user_id varchar (30),user_name varchar (21),\
    # password varchar (50),personal_tables varchar (1000),primary key(user_id))'
    # sql = 'drop table user_icon'
    # operator.update(sql)
    # operator.showField('user')
    # 建立用户icon表
    # sql = 'create table user_icon(user_id varchar (30) primary key,icon_name varchar (50),icon_type varchar (20),icon_content BLOB,\
    # foreign  key(user_id) references  user (user_id))'
    # operator.update(sql)
    # operator.showField('user_icon')
    md5 = MD5.MD5()
    path = r'D:/Learn-python-notes/projects/demo/Work/TCM_DSAS/userIcon/avatar.jpg'
    user_dict = {
        'user_id':'admin@qq.com',
        'user_name':'admin',
        'password':md5.md5Encode('123456'),
         'personal_tables':'',
         'icon_path':path
    }
    # operator.addUser(user_dict)
    operator.showTable('user')
    operator.showTable('user_icon')
