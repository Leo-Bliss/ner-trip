#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@Time    :    2021/4/29 0029 17:19
#@Author  :    tb_youth
#@FileName:    tcp_select_server.py
#@SoftWare:    PyCharm
#@Blog    :    https://blog.csdn.net/tb_youth

# socket使用select模型


import socket
import select

def start_server():
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    addr = ('127.0.0.1',8888)
    server.bind(addr)
    server.listen(5)

    inputs = [server]
    outputs = []
    while inputs:
        readable,writeable,exceptional = select.select(inputs,outputs,inputs)
        # 可读
        for s in readable:
            if s is server:
                conn,client_addr = s.accept()
                inputs.append(conn)
            else:
                data = s.recv(1024) # 接收客户端的消息
                if data:
                    print(data.decode('utf-8'))
                    if s not in outputs:
                        outputs.append(s) # 等下想发消息给客户端
                else: # 客户端断开了链接，做清理工作
                    if s in outputs:
                        outputs.remove(s)
                    inputs.remove(s)
                    s.close()

        # 可写
        for w in writeable:
            w.send('send msg'.encode('utf-8'))
            outputs.remove(w)

        # 异常
        for s in exceptional:
            inputs.remove(s)
            if s in outputs:
                outputs.remove(s)
            s.close()




if __name__ == '__main__':
    start_server()