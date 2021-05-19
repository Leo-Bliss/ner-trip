#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@Time    :    2021/4/29 0029 4:34
#@Author  :    tb_youth
#@FileName:    client_conn.py
#@SoftWare:    PyCharm
#@Blog    :    https://blog.csdn.net/tb_youth


import socket


class MsgContainer(object):
    def __init__(self,zere_count):
        self.zoro_count = zere_count # 前zero_count位作为数据长度标识
        self.msg_list = [] # 存接收到的数据处理后的数据（即去掉数据长度的信息）
        self.msg_len = 0 # 每一条消息的真实内容长度
        self.rcv_data = b'' # 接收数据缓存区

    def __build_head(self,str_len):
        ''' 构建消息头
        :param str_len: 消息真实内容长度 ，是字符串类型表示的
        :return:
        '''
        head = (self.zoro_count-len(str_len))*'0' + str_len
        return head.encode('utf-8')

    def pack_data(self,data):
        ''' 在data前加上长度信息
        data：需要传输的数据
        :return:
        '''
        bdata = data.encode('utf-8')
        str_len = len(bdata)
        return self.__build_head(str(str_len))+bdata

    def __get_msg_len(self):
        self.msg_len = int(self.rcv_data[:5]) # 收到数据前5位就是数据的真实内容长度

    def add_data(self,data):
        '''
        :param data: 这里的data是每次接收到的，不一定都有长度标识
        :return:
        '''
        if len(data)==0 or data is None:
            return
        self.rcv_data += data # 放到缓存区
        # 开始check是不是可以完整提取真实信息
        self.__check()

    def __check(self):
        '''
        检测是否可以完整提取真实信息了
        :return:
        '''
        if len(self.rcv_data)>self.zoro_count: # 首先除去长度信息还要内容
            self.__get_msg_len() # 获取到真实内容长度
            self.__get_msg() # 尝试提取

    def __get_msg(self):
        '''
        完整提取真实内容
        :return:
        '''
        if len(self.rcv_data)-self.zoro_count >= self.msg_len: # 已经可以完整提取真实内容
            msg = self.rcv_data[self.zoro_count:self.zoro_count+self.msg_len] # 提取
            self.rcv_data = self.rcv_data[self.zoro_count+self.msg_len:] # 被提取后更新接收缓存区
            msg = msg.decode('utf-8')
            self.msg_list.append(msg) # 提取出的真实内容放到消息队列
            self.__check() # 继续check
        else:
            return

    def get_all_msg(self):
        return self.msg_list

    def clear_all_msg(self):
        self.msg_list = []


def start_client():
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    addr = ('127.0.0.1',8888)
    client.connect(addr)
    mc = MsgContainer(5)
    while True:
        msg = '胃痛。胃痛。肝胃不和，气郁食滞。久病胃痛，经常发作，服香燥药不效，在外地疗养，现胃呆纳少，嗳气倒饱，胃脘胀痛，右肩背也痛，大便秘结，数日一次，小便可。行气疏郁，泄肝降胃。百合汤，抑气汤，交感丸，加减。乌药4.5克，百合12克，炒杭芍9克，获等9克，制香附9克，炒六曲4.5克，陈皮4.5克，火麻仁9克。水煎服。FALSE。肝郁气滞证。舌苔白滑，脉沉弦缓。万某，男，66岁，干部。1961年4月8日初诊。4月12日二诊:服药4剂，胃痛转好，大便通畅，右肩背仍痛，苔脉同前。按上方去麻仁，加枳壳4.5克，姜黄4.5克，炒麦芽6克。水煎服。4月16日三诊:服药5剂，胃痛止，纳食增，脘微胀，右肩背仍痛，舌苔薄白，边红，脉沉缓。拟丸药方常服。按二诊方加佛手9克，当归9克，用3倍量共研细末，用六曲糊为丸，如绿豆大，每晚服9克。吴少怀医案。《吴少怀医案》。'
        client.send(mc.pack_data(msg))
        rcv = client.recv(1024)
        if len(rcv)==0 or rcv is None:
            break
        mc.add_data(rcv)
        print('client recv ',mc.get_all_msg())

    client.close()



if __name__ == '__main__':
    start_client()

