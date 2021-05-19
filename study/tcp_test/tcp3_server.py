#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@Time    :    2021/4/29 0029 16:20
#@Author  :    tb_youth
#@FileName:    tcp3_server.py
#@SoftWare:    PyCharm
#@Blog    :    https://blog.csdn.net/tb_youth


import socket
import threading

def work(client_sock):
    while True:
        data = client_sock.recv(1024)
        if len(data)==0 or data is None:
            break
        data = data.decode('utf-8')
        print(data)
        info = '收到数据'
        client_sock.send(info.encode('utf-8'))
    client_sock.close()
    print(client_sock,' close')


def start_server():
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    addr = ('127.0.0.1',8888)
    server.bind(addr)
    server.listen(5)
    while True:
        conn,addr = server.accept()
        print(addr,' connected')
        t = threading.Thread(target=work,args=(conn,))
        t.start()


if __name__ == '__main__':
    start_server()