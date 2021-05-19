#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@Time    :    2021/4/29 0029 15:49
#@Author  :    tb_youth
#@FileName:    tcp2_client.py
#@SoftWare:    PyCharm
#@Blog    :    https://blog.csdn.net/tb_youth


import socket
from study.tcp_test.tcp_message import MsgContainer

def start_client():
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    # 服务器地址和端口
    host = socket.gethostbyname(socket.gethostname())
    print(host)
    port = 12345
    host = '127.0.0.1'
    port = 8888
    client.connect((host,port))
    mc = MsgContainer(5)
    while True:
        s = input()
        # if s == -1:
        #     break
        # data = 'I am client I am client I am client I am client I am client I am client I am client'
        data = str(s)
        fdata = mc.pack_data(data)
        client.send(fdata)
        while True:
            rcv = client.recv(1024)
            mc.add_data(rcv)
            if len(mc.get_all_msg()):
                ans = mc.get_all_msg()[0]
                print(ans)
                break
        mc.clear_all_msg()
    # client.close()


if __name__ == '__main__':
    start_client()