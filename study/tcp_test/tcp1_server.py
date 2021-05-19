#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@Time    :    2021/4/29 0029 13:28
#@Author  :    tb_youth
#@FileName:    tcp1_server.py
#@SoftWare:    PyCharm
#@Blog    :    https://blog.csdn.net/tb_youth


import socket

# 指定协议创建一个server端socket
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# socket.AF_INET : 服务器之间网络通信，socket.SOCK_STREAM：tcp,面向字节流
# socket.SOCK_DGRAM：udp,面向数据报

# 让端口可重复适用：意外死掉端口回收
server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

# 绑定ip和端口
server.bind(('127.0.0.1',8888))

# 监听:最大监听数量设置为1
server.listen(1)

# 等待客户端接入
client_sock,addr = server.accept()

# 接收客户端消息
data = client_sock.recv(1024)
print(data.decode('utf-8'))
client_sock.send(b'I am server,I have recv you msg')

# 关闭socket
client_sock.close()
server.close()