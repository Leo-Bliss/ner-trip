#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@Time    :    2021/4/20 0020 19:46
#@Author  :    tb_youth
#@FileName:    model_manager.py
#@SoftWare:    PyCharm
#@Blog    :    https://blog.csdn.net/tb_youth

import os
import sys
import time

import tensorflow as tf
import numpy as np

from preprocess.data_utils import  random_embedding, tag2label
from config.setting import PathConfig as path_cfg

from preprocess.utils import read_pkl, get_logger
from models.utils import get_Na_dct

CUR_PATH = os.path.abspath(os.path.dirname(__file__))
ROOT_PATH,_ = os.path.split(CUR_PATH)


from models.bilstm_crf2 import BiLSTM_CRF

class Args(object):
    train_data = path_cfg.inputs_path
    test_data = path_cfg.inputs_path
    batch_size = 64
    epoch = 40
    hidden_dim = 300
    optimizer = 'Adam'
    CRF = True
    lr = 0.5
    clip = 5.0
    dropout = 0.5
    update_embedding = True
    pretrain_embedding = 'random'
    embedding_dim = 300
    shuffle = True
    mode = 'train'
    demo_model = '1620921350'
    Na_dct = {}


class ModelManager(object):
    os.environ['CUDA_VISIBLE_DEVICES'] = '0'
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # default: 0
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    config.gpu_options.per_process_gpu_memory_fraction = 0.2  # need ~700MB GPU memory
    paths = {}
    model_path = None
    def __init__(self):
        self.args = Args()
        # test data info
        self.args.Na_dct = get_Na_dct(path_cfg.process_test_data_path,path_cfg.original_data_path)
        self.word2id = read_pkl(os.path.join(ROOT_PATH, self.args.train_data, 'word2id.pkl'))
        print('vocab_size:', len(self.word2id))
        self.embeddings = self.get_embedding()


    def set_model_id(self,id):
        '''

        :param id: mode id with str
        :return:
        '''
        self.args.demo_model = id

    def get_embedding(self):
        '''
        get char embeddings
        :return:
        '''
        if self.args.pretrain_embedding == 'random':
            embeddings = random_embedding(self.word2id, self.args.embedding_dim)
        else:
            embedding_path = 'pretrain_embedding.npy'
            embeddings = np.array(np.load(embedding_path), dtype='float32')
        return embeddings


    def init_path(self):
        '''
        paths setting
        :return:
        '''

        timestamp = str(int(time.time())) if self.args.mode == 'train' else self.args.demo_model
        print("model id : ",timestamp)
        output_path = os.path.join(ROOT_PATH, path_cfg.outputs_path, timestamp)
        if not os.path.exists(output_path): os.makedirs(output_path)
        summary_path = os.path.join(output_path, "summaries")
        self.paths['summary_path'] = summary_path
        if not os.path.exists(summary_path): os.makedirs(summary_path)
        self.model_path = os.path.join(output_path, "checkpoints/")
        if not os.path.exists(self.model_path): os.makedirs(self.model_path)
        # ckpt_prefix = os.path.join(self.model_path, "model")
        self.paths['model_path'] = self.model_path
        result_path = os.path.join(output_path, "results")
        self.paths['result_path'] = result_path
        if not os.path.exists(result_path): os.makedirs(result_path)
        log_path = os.path.join(result_path, "log.txt")
        self.paths['log_path'] = log_path
        get_logger(log_path).info(str(self.args))

    def get_model(self,way='create'):
        '''

        :param way: create or load
        :return:
        '''
        print(way)
        if way != 'create':
            ckpt_file = tf.train.latest_checkpoint(self.model_path)
            print(ckpt_file)
            self.paths['model_path'] = ckpt_file
        else:
            pass
        model = BiLSTM_CRF(self.args, self.embeddings, tag2label, self.word2id, self.paths, config=self.config)
        model.build_graph()
        return model

    def train(self):
        print('=' * 10, self.args.mode, '=' * 10)
        self.init_path()
        train_path = os.path.join(ROOT_PATH, self.args.train_data, 'train.pkl')
        test_path = os.path.join(ROOT_PATH, self.args.test_data, 'test.pkl')
        print("train data: ",train_path)
        print("test data: ", test_path)
        train_data = read_pkl(train_path)['train']
        test_data = read_pkl(test_path)['test']
        model = self.get_model(way='create')
        print("train data: {}".format(len(train_data)))
        model.train(train=train_data, dev=test_data)  #

    def test(self):
        self.args.mode = 'test'
        print('=' * 10, self.args.mode, '=' * 10)
        self.init_path()
        test_path = os.path.join(ROOT_PATH, self.args.test_data, 'test.pkl')
        test_data = read_pkl(test_path)['test']
        test_size = len(test_data)
        model = self.get_model(way='load')
        print("test data: {}".format(test_size))
        model.test(test_data)

    def input_line_predict(self):
        self.args.mode = 'predict'
        self.init_path()
        ckpt_file = tf.train.latest_checkpoint(self.model_path)
        model = self.get_model(way='load')
        saver = tf.train.Saver()
        with tf.Session(config=self.config) as sess:
            print('='*10,self.args.mode,'='*10)
            saver.restore(sess, ckpt_file)
            while (1):
                print('Please input your sentence:')
                demo_sent = input()
                if demo_sent == '' or demo_sent.isspace():
                    print('See you next time!')
                    break
                else:
                    demo_sent = list(demo_sent.strip())
                    demo_data = [(demo_sent, ['O'] * len(demo_sent))]
                    tag = model.demo_one(sess, demo_data)
                    print(tag)


    def line_predict(self, *args):
        if len(args) == 0 or not args[0]:
            return
        self.args.mode = 'predict'
        self.init_path()
        ckpt_file = tf.train.latest_checkpoint(self.model_path)
        model = self.get_model(way='load')
        saver = tf.train.Saver()
        with tf.Session(config=self.config) as sess:
            print('=' * 10, self.args.mode, '=' * 10)
            saver.restore(sess, ckpt_file)
            demo_sent = list(str(args[0]))
            demo_data = [(demo_sent, ['O'] * len(demo_sent))]
            tag = model.demo_one(sess, demo_data)
            print(tag)


if __name__ == '__main__':
    model_mgr = ModelManager()
    model_mgr.set_model_id('1620921350')
    model_mgr.test()