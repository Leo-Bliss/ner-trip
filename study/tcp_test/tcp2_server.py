#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@Time    :    2021/4/29 0029 13:52
#@Author  :    tb_youth
#@FileName:    tcp2_server.py
#@SoftWare:    PyCharm
#@Blog    :    https://blog.csdn.net/tb_youth


import socket
from study.tcp_test.tcp_message import MsgContainer

def start_server():
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    local_host =  socket.gethostbyname(socket.gethostname())
    print(local_host)
    port = 12345 # 0-65535
    server.bind((local_host,port))
    server.listen(5)
    print('server start.')
    mc = MsgContainer(5)
    while True:
        client_sock,addr = server.accept() # 获取到连接的 客户端的通信管道以及客户端地址
        print(f'{client_sock} : {addr} conn')
        while True:
            data = client_sock.recv(2)  # 每次接收2bytes
            if len(data) == 0:
                break
            mc.add_data(data)
            for msg in mc.get_all_msg():
                print(msg)
                info = 'rcv your info successfuly.'
                client_sock.send(mc.pack_data(info))
            mc.clear_all_msg()
        client_sock.close()


if __name__ == '__main__':
    start_server()





