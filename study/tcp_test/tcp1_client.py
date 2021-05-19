#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@Time    :    2021/4/29 0029 13:37
#@Author  :    tb_youth
#@FileName:    tcp1_client.py
#@SoftWare:    PyCharm
#@Blog    :    https://blog.csdn.net/tb_youth



import socket
import time

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host = '127.0.0.1'
port = 8888
addr = (host,port)
# 连接到服务器
client.connect(addr)
# 发送数据
client.send(b'I am client.')
# 接收服务端消息
data = client.recv(1024)
# 收到的都是byte型数据，解码
print(data.decode('utf-8'))
time.sleep(1)
client.close()

