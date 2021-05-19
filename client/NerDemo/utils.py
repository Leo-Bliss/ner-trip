#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@Time    :    2021/4/26 0026 14:01
#@Author  :    tb_youth
#@FileName:    utils.py
#@SoftWare:    PyCharm
#@Blog    :    https://blog.csdn.net/tb_youth


import re
import csv
import xlrd
from PyQt5.QtCore import QThread,pyqtSignal
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from  openpyxl import workbook
import pandas as pd
import json
import os


from chardet.universaldetector import UniversalDetector

CUR_PATH = os.path.abspath(os.path.dirname(__file__))

class CommonHelper():
    @staticmethod
    def readQSS(style_file):
        with open(style_file,'r',encoding='utf-8')as f:
            return  f.read()
    @staticmethod
    def get_file_encoding(file):
        with open(file,mode='rb') as f:
            detector = UniversalDetector()
            for line in f:
                detector.feed(line)
                if detector.done:
                    break
            detector.close()
            return detector.result['encoding']


    @staticmethod
    def get_split_index(txt_content, max_len=50):
        '''
        将文本切分成句子
        :param txt_content:
        :param max_len:短句子合并可达的最大长度,结合文本特征来确定
        :return: 切分index_list
        '''
        split_index_list = []
        pattern = '。|，|,|;|；|\.|\?'
        pre = 0
        pre_len = 0
        lens = len(txt_content)
        for id in re.finditer(pattern, txt_content):
            s, e = id.span()  # s为匹配内容的index,e为匹配内容下一个字符index(即另一段开始)
            now_len = e - pre
            if now_len + pre_len > max_len:  # 之前一段单独成段
                split_index_list.append(pre)
            else:  # 当前段和之前一段合并
                now_len = now_len + pre_len
            pre = e
            pre_len = now_len
        # 文本内容最后一定是切分点
        if not len(split_index_list) or split_index_list[-1] != lens + 1:
            split_index_list.append(lens)
        # print(lens)
        start = 0
        txt = ''
        for end in split_index_list:
            # print(txt_content[start:end])
            txt += txt_content[start:end]
            start = end
        assert txt == txt_content
        return split_index_list

    @staticmethod
    def get_mark_list(mark_data):
        length = len(mark_data)
        if length == 0:
            return
        left = 0
        mark_list = []
        while left < length:
            while left<length and mark_data[left][-1][0]!='B':
                left += 1
            content = ''
            if left<length:
                content += mark_data[left][0]
            else:
                break
            entity = mark_data[left][-1][2:]
            right = left+1
            while right<length and mark_data[right][-1][0]=='I' and mark_data[right][-1][2:]==entity:
                content += mark_data[right][0]
                right += 1
            start_pos,end_pos = left,right
            mark_list.append([entity,start_pos,end_pos,content])
            left = right
        return mark_list

    @staticmethod
    def build_view(mark_data,mark_list):
        view = []
        i,j = 0,0
        maxx = len(mark_list)
        length = len(mark_data)
        while i < length:
            if maxx==0 or j==maxx or i!=mark_list[j][1]:
                view.append([mark_data[i][0],'O'])
                i += 1
            else:
                view.append([mark_list[j][-1],mark_list[j][0]])
                i = mark_list[j][2]
                j += 1
        return view

    @staticmethod
    def get_entity_setting():
        setting_path = os.path.join(CUR_PATH, 'setting', 'entity.json')
        with open(setting_path, mode='r', encoding='utf-8') as f:
            txt = f.read()
        mp = json.loads(txt)
        return mp

    @staticmethod
    def write_viewjs(view,save_path):
        left = 'var leftdata = ['
        right = 'var rightdata = ['
        mp = CommonHelper().get_entity_setting()
        color = mp['entity-color']
        nk_entity = mp['nickname-entity']
        for item in view:
            txt = item[0]
            if txt == "\"":
                txt = "\\" + txt
            elif txt =="\\\n":
                continue
            left += '{' + 'text:"{}",'.format(txt) +  'title:"{}",'.format(nk_entity[item[-1]]) + 'color:"{}"'.format(color[item[-1]]) +'},'
        left += '];'
        for k,v in nk_entity.items():
            right += '{' + 'text:"{}",'.format(v) + 'title:"{}",'.format(v) + 'color:"{}"'.format(color[k]) + '},'
        right += '];'
        with open(save_path, mode='w', encoding='utf-8') as f:
            f.write(left)
            f.write('\n')
            f.write(right)







    @staticmethod
    def bioes2bio(mark_data):
        ans = []
        for item in mark_data:
            tmp = [item[0]]
            if item[-1][0] == 'S':
                tmp.append('B' + item[-1][1:])
            elif item[-1][0] == 'E':
                tmp.append('I' + item[-1][1:])
            else:
                tmp.append(item[-1])
            ans.append(tmp)
        return ans





class MsgContainer(object):
    '''
    用于解决粘包和分包问题
    '''
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


class ExcelHelper:
    def __init__(self):
        pass

    def read_excel(self,path):
        name, type = path.rsplit('.', maxsplit=1)
        if type == 'csv':
            with open(path, 'r',newline='',encoding='utf-8') as f:
                reader = csv.reader(f, delimiter=',')
                data = [line for line in reader]
                return data
        elif type in ['xlsx', 'xls']:
            workbook = xlrd.open_workbook(path)
            sheet1 = workbook.sheet_by_index(0)
            rows = len(sheet1.col_values(0))
            data = [sheet1.row_values(i) for i in range(rows)]
            return data
        else:
            print('{}文件格式不支持'.format(type))
            return -1


    def write_excel(self,file_path, data_list):
        try:
            wb = workbook.Workbook()
            wb.encoding = 'utf-8'
            wa = wb.active
            for item in data_list:
                wa.append(item)
            wb.save(file_path)
        except Exception as e:
            print(e)

class ReadFileThread(QThread):
    finished_signal = pyqtSignal(str)
    def __init__(self,file_name):
        super(ReadFileThread,self).__init__()
        self.file_name = file_name

    def run(self) -> None:
        common = CommonHelper()
        file_encoding = common.get_file_encoding(self.file_name)
        with open(self.file_name, mode='r', encoding=file_encoding) as f:
            file_type = self.file_name.rsplit('.', maxsplit=1)[-1]
            if file_type == 'txt':
                data = f.read()  # 小文件直接读，大文件可换成 for line in f
                self.finished_signal.emit(data)

class LoadToTableThread(QThread):
    finished_signal = pyqtSignal(QStandardItemModel,list,list)
    end_signal = pyqtSignal()
    def __init__(self,file_name):
        super(LoadToTableThread,self).__init__()
        self.file_name = file_name
        self.model = QStandardItemModel()

    def run(self) -> None:
        rows_data = self.get_rows()
        mark_data = [] # [[char,mark]]
        char_indexs = []
        start_index = 0
        for row in rows_data:
            tmp = []
            line= [QStandardItem(str(cell)) for cell in row]
            self.model.appendRow(line)
            for char in row:
                tmp.append(start_index)
                mark_data.append([char,'O'])
                start_index += 1
            char_indexs.append(tmp)
        self.finished_signal.emit(self.model,mark_data,char_indexs)
        self.end_signal.emit()

    def get_rows(self):
        common = CommonHelper()
        file_encoding = common.get_file_encoding(self.file_name)
        with open(self.file_name, mode='r', encoding=file_encoding) as f:
            file_type = self.file_name.rsplit('.', maxsplit=1)[-1]
            if file_type == 'txt':
                data = f.read()  # 小文件直接读，大文件可换成 for line in f
                split_indexs = common.get_split_index(data)
                pre = 0
                rows_data = []
                for e in split_indexs:
                    # print(data[pre:e])
                    rows_data.append(data[pre:e])
                    pre = e
                return rows_data

class WriteExcelThread(QThread):
    signal = pyqtSignal(str)
    end_signal = pyqtSignal()
    def __init__(self,mark_list,cols,save_path):
        super(WriteExcelThread,self).__init__()
        self.mark_list = mark_list
        self.cols = cols
        self.save_path = save_path


    def run(self) -> None:
        df = pd.DataFrame(data=self.mark_list,columns=self.cols)
        df.to_csv(self.save_path)
        self.signal.emit('保存成功')
        self.end_signal.emit()






if __name__ == '__main__':
    comm = CommonHelper()
    s = comm.bioes2bio([['1','E-FY'],['2','S-FY'],['3','B-FY']])
    print(s)



