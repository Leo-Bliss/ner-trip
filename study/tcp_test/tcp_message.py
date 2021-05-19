#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@Time    :    2021/4/29 0029 13:52
#@Author  :    tb_youth
#@FileName:    tcp_message.py
#@SoftWare:    PyCharm
#@Blog    :    https://blog.csdn.net/tb_youth



''''
简单解决tcp粘包与分包:在数据的最前面加上一个长度标识，指明本次要发送的数据长度是多少
小数据粘包： 每个小数据都有了长度标识，所以可以区分开来
大数据分包：大数据被分成好几段依次发送，最前面一段有这段数据长度的标识，只有达到这个长度才开始提取出信息
'''
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


if __name__ == '__main__':
    zero_count = 5
    data = 'I am mike'
    mc = MsgContainer(zero_count)
    print(mc.pack_data(data))

    # 模拟粘包
    recv = b'00009I am Mike' + b'00010I am Aikel' + b'00009I am Nike'
    mc.add_data(recv)
    msgs = mc.get_all_msg()
    for msg in msgs:
        print(msg)
    mc.clear_all_msg()

    # 模拟分包
    recv = b'00009I '
    mc.add_data(recv)
    recv = b'am Mike'
    mc.add_data(recv)
    mc.add_data(b'00008I ')
    mc.add_data(b'am Yam')
    print(mc.get_all_msg())




