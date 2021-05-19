#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@Time    :    2021/4/29 0029 4:22
#@Author  :    tb_youth
#@FileName:    server_start.py
#@SoftWare:    PyCharm
#@Blog    :    https://blog.csdn.net/tb_youth


import socket
import json
import threading
import tensorflow as tf


from net.utils import MsgContainer
from models.model_manager import ModelManager



class ModelServer(ModelManager):
    def __init__(self):
        super(ModelServer,self).__init__()
        pass


    def start(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.addr = ('127.0.0.1', 8888)
        self.server.bind(self.addr)
        self.server.listen(5)
        print('server start.')
        while True:
            conn, addr = self.server.accept()
            print(addr, ' connected')
            t = threading.Thread(target=self.work, args=(conn,))
            t.start()

    def work(self,client_sock):
        mc = MsgContainer(5)
        self.args.mode = 'predict'
        self.init_path()
        ckpt_file = tf.train.latest_checkpoint(self.model_path)
        self.model = self.get_model(way='load')
        saver = tf.train.Saver()
        with tf.Session(config=self.config) as sess:
            saver.restore(sess, ckpt_file)
            while True:
                data = client_sock.recv(1024)
                if len(data) == 0 or data is None:
                    break
                mc.add_data(data)
                msgs = mc.get_all_msg()
                if len(msgs):
                    ans = self.line_predict(msgs[0],sess)
                    dct = {'ans': ans}
                    msg = json.dumps(dct)
                    client_sock.send(mc.pack_data(msg))
                    mc.clear_all_msg()
            client_sock.close()
            print(client_sock, ' close')

    def line_predict(self,msg,sess):
        demo_sent = msg
        demo_data = [(demo_sent, ['O'] * len(demo_sent))]
        tag = self.model.demo_one(sess, demo_data)
        print(tag)
        return tag



if __name__ == '__main__':
    model_server = ModelServer()
    model_server.set_model_id('1620921350')
    model_server.start()