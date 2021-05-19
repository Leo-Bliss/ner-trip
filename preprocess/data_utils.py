#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@Time    :    2021/4/17 0017 15:41
#@Author  :    tb_youth
#@FileName:    data_utils.py
#@SoftWare:    PyCharm
#@Blog    :    https://blog.csdn.net/tb_youth
import argparse
import os
import pickle
import random
import sys
import copy
from glob import glob
import shutil


import re
import math
import multiprocessing
from collections import Counter
import pandas as pd
from jieba import posseg as psg # 用于获取 词性，词边界 特征
from cnradical import Radical,RunOption # 用于获取偏旁，拼音 特征
from tqdm import tqdm # 处理进度条
import numpy as np


from config.setting import PathConfig as path_cfg
from preprocess.utils import read_ann_file, read_txt_file, write_pkl, read_pkl


def count_entities(path=path_cfg.original_data_path):
    '''
    从原始数据.ann文件中获取所有实体类型
    :param path: 文件所在路径
    :return:
    '''
    entities_count_dict = {}
    files = [file for file in os.listdir(path) if file[-3:] == 'ann']
    for file in files:
        file_path = f'{path }/{file}'
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                entity_class = line.split('\t')[1].split(' ')[0]
                if entity_class not in entities_count_dict:
                    entities_count_dict[entity_class] = 1
                else:
                    entities_count_dict[entity_class] += 1

    save_path = f'{path_cfg.process_pkls_path}/entities_count.pkl'
    write_pkl(entities_count_dict, save_path)


def show_entities():
    # 所有源数据已标记的目标实体统计结果： entity_class:count
    path = f'{path_cfg.process_pkls_path}/entities_count.pkl'
    if  not os.path.exists(path):
        count_entities(path_cfg.original_data_path)
    entities_count_dict = read_pkl(path)
    print('total number of entity class:', len(entities_count_dict))
    print(entities_count_dict)


def get_word(txt_content):
    '''
    获取文本中每一个字符，构成列表返回
    :param txt_content:
    :return:
    '''
    word_list = [word for word in txt_content]
    return word_list


def get_entity_marked(file_name, file_path=path_cfg.original_data_path):
    '''
    获取已经标注的实体（目标实体）的实体类别和位置信息
    mark = [entity_name,start_pos,end_pos]
    end_pos: 是实体后一个字符的位置
    :param name: .ann原始数据文件名
    :return: marked_list
    '''
    file_path = f'{file_path}/{file_name}.ann'
    entity_marked_list = []
    lines = read_ann_file(file_path)
    for line in lines:
        item = line.split('\t')[1].split(' ')
        name, start, end = item[0], int(item[1]), int(item[-1])
        entity_marked_list.append([name, start, end])
    return entity_marked_list


def get_label(word_list, entity_marked_list, mode='BIO',data_from=None):
    '''
    采用标注mode=BIO or BIOES标注文本内容
    :param word_list:
    :param entity_marked_list:
    :param mode:
    :return: 标注好的标签列表
    '''
    # 先全部标注为'O'
    label_list = ['O' for item in word_list]
    # 再根据entity_marked_list标注目标实体：需要思考如何处理嵌套实体
    ''' 若出现嵌套实体，目前打算这样处理嵌套实体
    已经标注了的不再标注，记录下来放到extend文件夹中，
    构建训练集的时侯可前后取10个字左右标注好作为扩充语料用于训练
    '''

    ##############################################
    def check_marked(s, e):
        '''
        检测目标实体是否已经标记
        :param s: 开始位置
        :param e: 结束位置
        :return: True or False
        '''
        for i in range(s, e):
            if (label_list[i] != 'O'):
                return True
        return False

    ##############################################
    extend_marked_list = []  # 已标注中的嵌套实体，item = [entity_class,start,end]

    # ---------------------------------------------
    def bio_mark():
        for item in entity_marked_list:
            entity_class, start, end = item[0], item[1], item[-1]
            if (check_marked(start, end)):
                extend_marked_list.append([entity_class, start, end])
                continue
            label_list[start] = 'B-' + entity_class
            for i in range(start + 1, end):
                label_list[i] = 'I-' + entity_class

    def bioes_mark():
        for item in entity_marked_list:
            entity_class, start, end = item[0], item[1], item[-1]
            if (check_marked(start, end)):
                extend_marked_list.append([entity_class, start, end])
                continue
            if (end - start == 1):  # 单个字符的实体：S-entity_class
                label_list[start] = 'S-' + entity_class
            else:  # 多个字符的实体：B(I)E-entity_class
                label_list[start] = 'B-' + entity_class
                label_list[end - 1] = 'E-' + entity_class
                for i in range(start + 1, end - 1):
                    label_list[i] = 'I-' + entity_class
    # ---------------------------------------------
    bio_mark() if mode == 'BIO:' else bioes_mark()
    if len(extend_marked_list) and data_from:
        print('extend_marked : ', extend_marked_list)
        write_extend_file(data_from, extend_marked_list)
    return label_list


def write_extend_file(file_name, extend_marked_list):
    '''
    未标注的嵌套'子’实体信息先写到extend文件
    :param file_name:
    :param extend_marked_list:
    :return:
    '''
    file_path = f'{path_cfg.extend_data_path}/{file_name}.csv'
    df = pd.DataFrame(extend_marked_list)
    df.to_csv(file_path, index=False, encoding='utf-8', header=None)


def get_flag_bound(txt_content):
    '''
    采用jieba分词工具提取词性（flag）和词边界(bound)特征
    :param txt_content:
    :return:
    '''
    start = 0
    flag_list = ['x' for item in txt_content]  # 词性先全部打上’x'
    bound_list = ['M' for item in txt_content]  # 词边界先全部打上‘M’
    for word, flag in psg.cut(txt_content):
        length = len(word)
        # 词性：词的每个字打上词性flag
        for i in range(start, start + length):
            flag_list[i] = flag
        # 词边界
        if (length == 1):
            bound_list[start] = 'S'
        else:
            bound_list[start] = 'B'
            bound_list[start + length - 1] = 'E'
        start += length
    return flag_list, bound_list


def get_radical_pinyin(txt_content, unknown_flag='UNK'):
    '''
    获取偏旁和拼音特征
    :param txt_content:
    :return:
    '''
    #########################################################
    def trans_aim(trans_method, unknown_flag):
        '''
        偏旁和拼音特征转换
        :param trans_method:  转换方法
        :param unknown_flag: 未知标记符
        :return:
        '''
        aim_list = []
        for ch in txt_content:
            tmp = trans_method.trans_ch(ch)
            aim_list.append(tmp if tmp is not None else unknown_flag)
        return aim_list
    #########################################################
    radical = Radical(RunOption.Radical)
    pinyin = Radical(RunOption.Pinyin)
    # 偏旁特征，无偏旁的使用UNK（Unknow Key）
    radical_list = trans_aim(radical, unknown_flag)
    # 拼音特征，无拼音的使用UNK
    pinyin_list = trans_aim(pinyin, unknown_flag)
    return radical_list, pinyin_list


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
        if now_len + pre_len > max_len and pre:  # 之前一段单独成段
            split_index_list.append(pre)
        else:  # 当前段和之前一段合并
            now_len = now_len + pre_len
        pre = e
        pre_len = now_len
    list_len = len(split_index_list)
    # 文本内容最后一定是切分点
    if not list_len or (list_len and split_index_list[-1]!=lens + 1):
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


def process_one_file(file_name, data_class='train', cut_flag='seg'):
    src_path = f'{path_cfg.original_data_path}/{file_name}.txt'
    txt = read_txt_file(src_path)
    word = get_word(txt)
    mkd = get_entity_marked(file_name)
    label = get_label(word, mkd,data_from=file_name,mode='BIOES')
    flag, bound = get_flag_bound(txt)
    radical, pinyin = get_radical_pinyin(txt)
    # 统一截断
    split_index = get_split_index(txt)
    sub_word_list = []
    sub_label_list = []
    sub_flag_list = []
    sub_bound_list = []
    sub_radical_list = []
    sub_pinyin_list = []
    start = 0
    samples = 0  # 样本数：即一个txt被切分成了多少句话
    for end in split_index:
        sub_word_list.append(word[start:end])
        sub_label_list.append(label[start:end])
        sub_flag_list.append(flag[start:end])
        sub_bound_list.append(bound[start:end])
        sub_radical_list.append(radical[start:end])
        sub_pinyin_list.append(pinyin[start:end])
        samples += 1
        start = end
    data_dic = {
        'word': sub_word_list,
        'label': sub_label_list,
        'bound': sub_bound_list,
        'flag': sub_flag_list,
        'radical': sub_radical_list,
        'pinyin': sub_pinyin_list
    }
    cols = len(data_dic.keys())  # 列数：即特征个数
    # print(data_dic)
    dataset = []
    for i in range(samples):
        records = list(zip(*[list(v[i]) for v in data_dic.values()]))  # *解压,不加*是压缩
        dataset += records + [[cut_flag] * cols]  # 每存完一个句子需要一行cut_flag进行隔离
    # print(dataset)
    dataset = pd.DataFrame(dataset, columns=data_dic.keys())  # 转换成dataframe
    # print(dataset)
    save_path = f'{path_cfg.process_data_path}/{data_class}/{file_name}.csv'
    dataset.to_csv(save_path, index=False, encoding='utf-8', columns=None)


def process_multi_files(train_rate=0.8):
    # 获取所有文件名：不含文件类型后缀
    file_names = list(set(file.split('.')[0] for file in os.listdir(path_cfg.original_data_path)))
    if len(file_names) == 0:
        return
    # 打乱顺序
    random.shuffle(file_names)
    # 划分训练集，测试集
    length = len(file_names)
    train_cnt = int(length * train_rate)
    train_files = file_names[:train_cnt]
    test_files = file_names[train_cnt:]
    # 多进程处理文件
    cpu_cnt = multiprocessing.cpu_count()
    # print('cpu_cnt = ', cpu_cnt)
    # 进程池
    pool = multiprocessing.Pool(cpu_cnt)

    ###########################################################################
    def process(files, data_class):
        for name in files:
            pool.apply_async(process_one_file, args=(name, data_class))
    ###########################################################################
    process(train_files, 'train')
    process(test_files, 'test')
    pool.close()
    pool.join()
    print('All subprocesses done.')


def judge_char(ch):
    if ch.isdigit():
        return 'NUM'
    elif (u'\u0041' <= ch <= u'\u005a') or (u'\u0061' <= ch <= u'\u007a'):
        # 注意这里不能使用isalpha，isalpha：字符串至少有一个字符并且所有字符都是字母则返回 True
        return 'ENG'
    elif ch == r'\n':
        return 'BCSP' # backspace
    elif ch in [' ', '\t', '\u2003']:
        return'SPCE'
    else:
        return ch


def bimapping(data, min_freq=1, is_word=False, seg_flag='seg', is_label=False):
    '''
    构建双向映射
    :param data:
    :param min_freq:
    :param is_word:
    :param sep:
    :param is_label:
    :return:
    '''
    mp = {}
    for item in data:
        if item == seg_flag:  # 分割标记符不要
            continue
        if is_word:  # 字符构建字典时可以预处理一下某类字符，即可缩小字典规模也有利于后期的识别工作
            item = judge_char(item)
        mp[item] = mp[item] + 1 if item in mp.keys() else 1
    if not is_label:
        mp['PAD'] = sys.maxsize  # PAD:句子长度不一样时用于填充
    else:
        mp['O'] = sys.maxsize  # 这里也可以不需要，O肯定是最多的，填充的内容的label设置为O
    if is_word:
        mp['UNK'] = sys.maxsize - 1  # UNK:未登录词
    data = sorted(mp.items(), key=lambda x: x[1], reverse=True)  # 按出现频率降序排列
    # data = [x[0] for x in data if x[1]>=min_freq]  # 去掉频率小于min_freq的元素 ： '未登录词'
    id2item = []
    lowfreq_dict = {}
    for x in data:
        if x[1] >= min_freq:
            id2item.append(x[0])
        else:
            lowfreq_dict[x[0]] = x[1]
    item2id = {v: i for i, v in enumerate(id2item)}
    if is_word:
        save_path = f'{path_cfg.process_pkls_path}/lowfreq_words.pkl'
        write_pkl(lowfreq_dict, save_path)
    return id2item, item2id

def build_fetures_dict():
    ''''
    将word,label,bound,flag,radical,pinyin中字符与数字建立互相映射，
    即初步将字符转化为数字，后续用于词嵌入
    '''
    all_dict = {}
    # 首先读取到process下所有的csv文件
    pattern = '*.csv'
    train_files = glob(f'{path_cfg.process_train_data_path}/{pattern}')
    test_files = glob(f'{path_cfg.process_test_data_path}/{pattern}')
    files = train_files +  test_files
    all_w,all_bound,all_flag,all_label,all_radical,all_pinyin=[],[],[],[],[],[]
    for file in tqdm(files):
        df = pd.read_csv(file,sep=',')
        all_w += df['word'].tolist()
        all_bound += df['bound'].tolist()
        all_flag += df['flag'].tolist()
        all_label += df['label'].tolist()
        all_radical += df['radical'].tolist()
        all_pinyin += df['pinyin'].tolist()
    all_dict['word'] = bimapping(all_w,min_freq=3,is_word=True) # 对于中医词汇删去低频词感觉不太好，不删影响却不大
    all_dict['label'] = bimapping(all_label,is_label=True)
    all_dict['bound'] = bimapping(all_bound)
    all_dict['flag'] = bimapping(all_flag)
    all_dict['radical'] = bimapping(all_radical)
    all_dict['pinyin'] = bimapping(all_pinyin)
    # 将字典写为二进制文件
    dst_path = f'{path_cfg.process_pkls_path}/fetures_dict.pkl'
    write_pkl(all_dict,dst_path)

def get_fetures_dict():
    src_path = f'{path_cfg.process_pkls_path}/fetures_dict.pkl'
    if not os.path.exists(src_path):
        build_fetures_dict()
    fetures_dict = read_pkl(src_path)
    return fetures_dict

def get_lowfreq_words():
    src_path = f'{path_cfg.process_pkls_path}/lowfreq_words.pkl'
    if not os.path.exists(src_path):
        return -1
    print(read_pkl(src_path))



def item2id(data,mp,feture=None):
    '''
    data中字符根据mp映射成数字（id）
    :param data:
    :param mp:
    :return:
    '''
    if feture=='word':
        res = []
        for ch in data:
            ch = judge_char(ch)
            key =  ch if ch in mp else 'UNK'
            res.append(mp[key])
        return res
    else:
        return [mp[x] if x in mp else mp['UNK'] for x in data]


def build_df_dict():
    '''
    构建字符的文档频率字典
    :return:
    '''
    w2id = get_fetures_dict()['word'][1]
    root = path_cfg.process_train_data_path
    files = list(os.listdir(root))
    df_mp = {}  # w_id : tdf
    for file in tqdm(files):
        path = os.path.join(root, file)
        sample = pd.read_csv(path, sep=',')
        for w in set(sample['word'].tolist()):
            ch = judge_char(w)
            if ch not in w2id.keys():
                ch = 'UNK'
            w_id = w2id[ch]
            df_mp[w_id] = df_mp[w_id]+1 if w_id in df_mp else 1
    save_path = f'{path_cfg.process_pkls_path}/df_count.pkl'
    write_pkl(df_mp,save_path)


def get_df_dict():
    src_path = f'{path_cfg.process_pkls_path}/df_count.pkl'
    if not os.path.exists(src_path):
        build_df_dict()
    df_dict = read_pkl(src_path)
    return df_dict



def get_one_file_tfidf(word_ids):
    '''
    一个文挡中的字符的tfidf
    :param word_ids:
    :return:
    '''
    df_dict = get_df_dict()
    N = len(os.listdir(path_cfg.process_train_data_path)) # 训练集文档数
    ftotal = len(word_ids)
    wf_dict = Counter(word_ids)
    tfidf_list = []
    for w_id in word_ids:
        tf = wf_dict[w_id]/ftotal # 该词在本文档中出现几次,最好做归一化，即：该词在本文档词频/本文档词总数
        df = df_dict[w_id] # 该词在几个文档中出现
        idf = math.log(N/df) # 逆文档频率
        tfidf_list.append(tf*idf)
    return tfidf_list


class DataAugmentation(object):
    ''' 文本数据增强的思路：
    1. 【同义词】替换、插入、交换和删除
    2. 切分 重新 交叉拼接
    3. 随机遮盖文本中某些词
    4. 非核心词替换（用词典中不重要的词去替换文本中一定比例的不重要词，【TF-IDF】值来衡量一个词对于一段文本的重要性）
    5. 翻译后回译
    '''
    # 数据增强放到拆分句子的时候来做是比较好的，除了思路2，其他的思路在后面实现起来复杂
    def __init__(self):
        pass

    @staticmethod
    def repalce_by_twin():
        '''思路1：同义词替换
        twin : similar words
        :return:
        '''
        pass

    @staticmethod
    def slipce_by_slide_windows(sequence_list, window_size, shuffle=False):
        '''思路2【简化版本】：文本切分 重新 （交叉）拼接
        :param sequence_list: 句子列表（可以是一个文件中的，多个文件中的也可以！）
        :param window_size: 窗口大小为window_size个句子进行滑动
        :param shuffle: 提前随机打乱各句子顺序（也可以拼接时打乱，但是无论是时间还是空间复杂度都会增加，总体效果却差不多）
        这里的句子是之前切分好的，可以做更细粒度的切分；shuffle = True相当于交叉拼接。
        :return:
        '''
        cpy_list = copy.deepcopy(sequence_list) # 保证不修改外部传入的数据，这里深拷贝一份
        seq_nums = len(cpy_list)
        assert seq_nums>0
        if window_size >= seq_nums:
            return None
        fet_nums = len(cpy_list[0])
        if shuffle:
            random.shuffle(cpy_list)
        res = []
        left = right = 0
        left_end = seq_nums - window_size
        while left <= left_end:
            # right右滑动
            while right-left+1 <= window_size:
                right += 1
            # 拼接成一段
            item = []
            for i in range(fet_nums):
                tmp = []
                for j in range(left, right):
                    tmp.extend(cpy_list[j][i])
                item.append(tmp)
            res.append(item)
            # left 右滑动
            left += 1
        return res

    @staticmethod
    def random_veil():
        ''' 思路3：随机遮盖文本中某些词
        veil : something to hide word
        这里也可结合tfidf进行随机（主要是对非核心词进行掩盖，识别目标是核心词）
        :return:
        '''
        pass

    @staticmethod
    def replace_by_importance(result):
        ''' 思路4：非核心词替换
        importance of word : 最简单的是对'O'标签的字符替换；而这里打算采用tfidf
        :return:
        '''
        tfidf_list = get_one_file_tfidf(result[0])
        print(tfidf_list)
        pass



def build_data(name='train',seg_flag='seg',data_augmentation=False):
    all_dict = get_fetures_dict()
    results = []
    root = f'{path_cfg.process_data_path}/{name}'
    files = list(os.listdir(root))
    for file in tqdm(files):
        result = []
        path = os.path.join(root,file)
        sample = pd.read_csv(path,sep=',')
        # 获取到切分符位置index
        sep_index = sample[sample['word']==seg_flag].index.to_list()
        # 获取句子并转换为id
        start = 0
        for end in sep_index:
            item = []
            for feature in sample.columns:
                item.append(item2id(list(sample[feature])[start:end], all_dict[feature][1],feature))
            start = end + 1
            result.append(item)
        results.extend(result)

        if data_augmentation:
            da = DataAugmentation()
            # 两个句子拼接（窗口大小为两个句子进行滑动）
            two = da.slipce_by_slide_windows(result,window_size=2)
            if two:
                results.extend(two)
                results.extend(da.slipce_by_slide_windows(result,window_size=2,shuffle=True))
            # 三个句子拼接
            three = da.slipce_by_slide_windows(result,window_size=3)
            if three:
                results.extend(three)
    # results写入二进制文件中
    dst_path = f'{path_cfg.process_pkls_path}/{name}.pkl'
    write_pkl(results, dst_path)
    print(f'{name}.pkl finished.')

def process_input_txt(txt):
    '''
    处理通过外部输入的文本，
    根据特征映射成对应id
    :param txt:
    :return:
    '''
    all_dict = get_fetures_dict()
    word = get_word(txt)
    # label = get_label(word, mkd)
    flag, bound = get_flag_bound(txt)
    radical, pinyin = get_radical_pinyin(txt)
    # 统一截断
    split_index = get_split_index(txt)
    result = []
    start = 0
    # samples = 0  # 样本数：即一个txt被切分成了多少句话
    for end in split_index:
        print(word[start:end])
        word_id = item2id(word[start:end], all_dict['word'][1],feture='word')
        label_id = item2id(['O'] * (end - start), all_dict['label'][1])
        bound_id = item2id(bound[start:end], all_dict['bound'][1])
        flag_id = item2id(flag[start:end], all_dict['flag'][1])
        radical_id = item2id(radical[start:end], all_dict['radical'][1])
        pinyin_id = item2id(pinyin[start:end], all_dict['pinyin'][1])
        result.append([word_id, label_id, bound_id, flag_id, radical_id, pinyin_id])
        # samples += 1
        start = end
    # print(samples)
    return result

class BatchManager(object):

    def __init__(self,batch_size,name='train',data=None):
        '''

        :param batch_size: 每次投喂的数量
        :param name:
        '''
        self.data = self.read_data(name) if name!='input' else data
        self.batch_data = self.sort_and_pad(self.data, batch_size,name)
        self.len_data = len(self.batch_data)

    def read_data(self,name):
        with open(f'{path_cfg.process_data_path}/pkls/{name}.pkl', 'rb') as f:
            return pickle.load(f)

    def sort_and_pad(self, data, batch_size,name):
        num_batch = int(math.ceil(len(data) / batch_size)) # 总共多少个批次
        sorted_data = data if name == 'input' else sorted(data, key=lambda x: len(x[0])) # 按句子长度排序:后续需要根据句子长度填充PAD
        batch_data = list()
        for i in range(num_batch):
            batch_data.append(self.pad_data(sorted_data[i * int(batch_size): (i+1) * int(batch_size)]))
        return batch_data

    @staticmethod
    def pad_data(data):
        chars = []
        targets = []
        bounds = []
        flags = []
        radicals = []
        pinyins = []
        max_length = max([len(sentence[0]) for sentence in data])  # len(data[-1][0])
        for line in data:
            char,target,bound,flag,radical,pinyin, = line
            padding = [0] * (max_length - len(char)) # PAD--0
            chars.append(char + padding)
            targets.append(target + padding)
            bounds.append(bound + padding)
            flags.append(flag + padding)
            radicals.append(radical + padding)
            pinyins.append(pinyin+padding)
        return [chars,targets,bounds,flags,radicals,pinyins]

    def iter_batch(self, shuffle=False):
        if shuffle:
            random.shuffle(self.batch_data)
        for idx in range(self.len_data):
            yield self.batch_data[idx]



## tags, BIOES
tag2label = {'O': 0, 'B-FY': 1, 'I-FY': 2, 'E-FY': 3, 'S-FY': 4,
             'B-FJ': 5, 'I-FJ': 6, 'E-FJ': 7, 'S-FJ': 8, 'B-ZH': 9,
             'I-ZH': 10, 'E-ZH': 11, 'S-ZH': 12, 'B-ZZ': 13,
             'I-ZZ': 14, 'E-ZZ': 15, 'S-ZZ': 16, 'B-SX': 17, 'I-SX': 18,
             'E-SX': 19, 'S-SX': 20, 'B-MX': 21, 'I-MX': 22,
             'E-MX': 23, 'S-MX': 24, 'B-ZF': 25, 'I-ZF': 26, 'E-ZF': 27, 'S-ZF': 28}





def sentence2id(sent, word2id):
    """

    :param sent:
    :param word2id:
    :return:
    """
    sentence_id = []
    for word in sent:
        word = judge_char(word)
        if word not in word2id:
            word = 'UNK'
        sentence_id.append(word2id[word])
    return sentence_id


def read_dictionary(vocab_path):
    """

    :param vocab_path:
    :return:
    """
    vocab_path = os.path.join(vocab_path)
    word2id = read_pkl(vocab_path)
    print('vocab_size:', len(word2id))
    return word2id


def random_embedding(vocab, embedding_dim):
    """

    :param vocab:
    :param embedding_dim:
    :return:
    """
    embedding_mat = np.random.uniform(-0.25, 0.25, (len(vocab), embedding_dim))
    embedding_mat = np.float32(embedding_mat)
    return embedding_mat



def pad_sequences(sequences, pad_mark=0):
    """

    :param sequences:
    :param pad_mark:
    :return:
    """
    max_len = max(map(lambda x : len(x), sequences))
    seq_list, seq_len_list = [], []
    for seq in sequences:
        seq = list(seq)
        seq_ = seq[:max_len] + [pad_mark] * max(max_len - len(seq), 0)
        seq_list.append(seq_)
        seq_len_list.append(min(len(seq), max_len))
    return seq_list, seq_len_list


def batch_yield(data, batch_size, vocab, tag2label, shuffle=False):
    """

    :param data:
    :param batch_size:
    :param vocab:
    :param tag2label:
    :param shuffle:
    :return:
    """
    if shuffle:
        random.shuffle(data)

    seqs, labels = [], []
    for [sent_, tag_] in data:
        sent_ = sentence2id(sent_, vocab)
        label_ = [tag2label[tag] for tag in tag_]

        if len(seqs) == batch_size:
            yield seqs, labels
            seqs, labels = [], []

        seqs.append(sent_)
        labels.append(label_)

    if len(seqs) != 0:
        yield seqs, labels


def str2bool(v):
    # copy from StackOverflow
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

if __name__ == '__main__':
    # get_lowfreq_words()
    # build_df_dict()
    # build_data(name='train',data_augmentation=False)
    # a = [1,2,3]
    # b = [4,6,9]
    # c = [7,8,5]
    # x = [a,b,c]
    # random.shuffle(x)
    # print(x)
    pass

