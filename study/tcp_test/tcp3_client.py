#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@Time    :    2021/4/29 0029 16:33
#@Author  :    tb_youth
#@FileName:    tcp3_client.py
#@SoftWare:    PyCharm
#@Blog    :    https://blog.csdn.net/tb_youth

import socket
import os
import time




def start_client():
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    addr = ('39.108.189.168',8801)
    client.connect(addr)
    count = 0
    while True:
        msg = 'client  pid : {}'.format(os.getpid())
        client.send(msg.encode('utf-8'))
        rcv = client.recv(1024)
        print('client recv ',rcv.decode('utf-8'))
        time.sleep(3)
        count += 1
        if count > 20:
            break
    client.close()



if __name__ == '__main__':
    start_client()

