#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@Time    :    2021/4/13 0013 14:51
#@Author  :    tb_youth
#@FileName:    bilstm_crf.py
#@SoftWare:    PyCharm
#@Blog    :    https://blog.csdn.net/tb_youth

'''
这份代码有问题,
服务器弃用该代码，
仅留着用于学习
'''

import tensorflow as tf
import numpy as np
from tensorflow.contrib import rnn
from tensorflow.contrib import crf


def network(inputs,shapes,num_tags,hidden_dim=100,initializer=tf.truncated_normal_initializer(),dropout_rate=0.5):
    '''

    :param inputs:
    :param shapes:
    :param num_tags:
    :param hidden_dim:  隐藏层维度
    :param initializer:
    :return:
    '''
    # 特征嵌入：将所有特征id转换成固定长度向量
    embedding = []
    keys = list(shapes.keys())
    for key in keys:
        with tf.variable_scope(key+'_embedding'):
            lookup = tf.get_variable(
                name = key+'_embedding',
                shape = shapes[key],
                initializer = initializer
            )
            embedding.append(tf.nn.embedding_lookup(lookup,inputs[key])) # 这里可以考虑lookup训练好的字向量
            '''
            字符id转化成向量，这里的字向量是在模型中训练得到，也可以预训练好作为输入
            embedding_lookup 类似与查表，input中的值作为被查表的索引，这个函数就是通过字符id来构建字向量
            '''

    embed = tf.concat(embedding,axis=-1) # shape [None,None,char_dim+..+pinyin_dim]

    # 求出每个句子的真实长度:属于真实的句子的id一定>0,填充的为PAD,其id=0,UNK的id是未登录词id
    sign = tf.sign(tf.abs(inputs[keys[0]]))
    # sign为>0（1）的个数即为真实序列长度
    length = tf.reduce_sum(sign,reduction_indices=1)
    num_time = tf.shape(inputs[keys[0]])[1] # 填充之后序列长度
    # （双层）RNN编码
    with tf.variable_scope('Bilstm_layer1'):
        lstm_cell = {}
        for name in ['forword','backword']:
            with tf.variable_scope(name):
                lstm_cell[name] = rnn.BasicLSTMCell(
                    hidden_dim # 隐藏层维度：隐藏层神经元个数
                )
        outputs1,finial_states1 = tf.nn.bidirectional_dynamic_rnn(
            lstm_cell['forword'],
            lstm_cell['backword'],
            embed, # 输入
            dtype = tf.float32,
            sequence_length = length
        )
        outputs1 = tf.concat(outputs1,axis=-1) # output_fw_seq, output_bw_seq: b,L,2*hidden_dim
        # outputs1 = tf.nn.dropout(outputs1,dropout_rate) # dropout：为了防止过拟合的

        with tf.variable_scope('Bilstm_layer2'):
            lstm_cell = {}
            for name in ['forword', 'backword']:
                with tf.variable_scope(name):
                    lstm_cell[name] = rnn.BasicLSTMCell(
                        hidden_dim  # 神经元个数
                    )
            outputs, finial_states1 = tf.nn.bidirectional_dynamic_rnn( # bidirectional 代表使用双向LSTM
                lstm_cell['forword'],
                lstm_cell['backword'],
                outputs1, # 输入：注意这里是用Bilstm_layer1的输出
                dtype=tf.float32,
                sequence_length=length
            )
        output = tf.concat(outputs, axis=-1)
        # output = tf.nn.dropout(output,dropout_rate)
        # 输出映射
        output = tf.reshape(output,[-1,2*hidden_dim])
        with tf.variable_scope('project_layer1'):
            w = tf.get_variable(
                name = 'w',
                shape = [2*hidden_dim,hidden_dim],
                initializer = initializer
            )
            b= tf.get_variable(
                name = 'b',
                shape = [hidden_dim],
                initializer = tf.zeros_initializer()
            )
            output = tf.nn.relu(tf.matmul(output,w) + b) #tf.nn.relu()函数的目的是，将输入小于0的值幅值为0，输入大于0的值不变
        with tf.variable_scope('project_layer2'):
            w = tf.get_variable(
                name = 'w',
                shape = [hidden_dim,num_tags],
                initializer = initializer
            )
            b= tf.get_variable(
                name = 'b',
                shape = [num_tags],
                initializer = tf.zeros_initializer()
            )
            output = tf.matmul(output,w) + b
        output = tf.reshape(output,[-1,num_time,num_tags])
        return output,length # batch_size,maxlength,2*hidden_dim

class BiLSTM_CRF(object):
    def __init__(self,all_dict):
        self.mp = all_dict
        # 需要用到的参数
        self.num_char = len(all_dict['word'][0])
        # self.num_bound = len(all_dict['bound'][0])
        # self.num_flag = len(all_dict['flag'][0])
        # self.num_radical = len(all_dict['radical'][0])
        # self.num_pinyin = len(all_dict['pinyin'][0])
        self.num_tags = len(all_dict['label'][0])
        # 以下参数可以自己设置
        ########################
        self.char_dim = 300 # 100-300为宜
        # self.bound_dim = 20
        # self.flag_dim = 50
        # self.radical_dim = 50
        # self.pinyin_dim = 50
        self.hidden_dim = 300
        self.learning_rate = 0.0001 # 学习率
        self.clip_value = 5 # 梯度截断
        # dropout解决：模型的参数太多，而训练样本又太少，训练出来的模型很容易产生过拟合的现象
        # 前向传播的时候，让某个神经元的激活值以一定的概率p停止工作
        self.dropout_rate = 0.5
        ########################
        # 定义接收数据的placeholder
        self.char_inputs = tf.placeholder(dtype=tf.int32,shape=[None,None],name='char_inputs')
        # self.bound_inputs = tf.placeholder(dtype=tf.int32, shape=[None, None], name='bound_inputs')
        # self.flag_inputs = tf.placeholder(dtype=tf.int32, shape=[None, None], name='flag_inputs')
        # self.radical_inputs = tf.placeholder(dtype=tf.int32, shape=[None, None], name='radical_inputs')
        # self.pinyin_inputs = tf.placeholder(dtype=tf.int32, shape=[None, None], name='pinyin_inputs')
        self.targets = tf.placeholder(dtype=tf.int32, shape=[None, None], name='targets')

        self.global_step = tf.Variable(0,trainable=False) # 不需要训练，只是用来计数

        # 计算模型输出
        self.logits,self.length = self.get_logits(self.char_inputs)
        # 计算损失
        self.cost = self.loss(self.logits,self.targets,self.length)
        # 采用梯度截断优化(解决梯度爆炸)：将所有的参数剪裁到 [-clip_value, clip_value]
        with tf.variable_scope('optimizer'):
            # 这里采用Adadelta优化器，其他优化器：Adagrad，Adam,Momentum，SGD...
            #opt = tf.train.AdadeltaOptimizer(self.learning_rate)
            opt = tf.train.AdamOptimizer(self.learning_rate)
            grad_vars = opt.compute_gradients(self.cost) # 计算出所有参数的导数
            clip_grad_vars = [[tf.clip_by_value(g,-self.clip_value,self.clip_value),v] for g,v in grad_vars] # 得到截断之后的梯度
            self.train_op = opt.apply_gradients(clip_grad_vars,self.global_step) # 使用截断后的参数用于梯度更新
        self.saver = tf.train.Saver(tf.global_variables(),max_to_keep=5) # 模型保存器


    def get_logits(self,char):
        '''接收一批样本的特征数据，计算出网络的输出值
        :param char: type of int,id of char a tensor of shape 2-D[None,None]
        :param bound:
        :param flag:
        :param radical:
        :param pinyin:
        :return:
        '''
        inputs = {
            'char': char,
            # 'bound': bound,
            # 'flag': flag,
            # 'radical': radical,
            # 'pinyin': pinyin
        }
        shapes = {
            'char':[self.num_char,self.char_dim],
            # 'bound':[self.num_bound,self.bound_dim],
            # 'flag':[self.num_flag,self.flag_dim],
            # 'radical':[self.num_radical,self.radical_dim],
            # 'pinyin':[self.num_pinyin,self.pinyin_dim]
        }
        return network(inputs, shapes, self.num_tags, self.hidden_dim,dropout_rate=self.dropout_rate)

    def loss(self,output,targets,lengths):
        b = tf.shape(lengths)[0]
        num_steps = tf.shape(output)[1]
        with tf.variable_scope('crf_loss'):
            small = -1000.0
            start_logits = tf.concat(
                [small*tf.ones(shape=[b,1,self.num_tags]),tf.zeros(shape=[b,1,1])],axis=-1
            )
            pad_logits = tf.cast(small*tf.ones([b,num_steps,1]),tf.float32)
            logits = tf.concat([output,pad_logits],axis=-1)
            logits = tf.concat([start_logits,logits],axis=1)
            targets = tf.concat(
                [tf.cast(self.num_tags*tf.ones([b,1]),tf.int32),targets],axis=-1
            )
            self.trans = tf.get_variable(
                name = 'trans',
                shape = [self.num_tags+1,self.num_tags+1],
                initializer=tf.truncated_normal_initializer()
            )
            # CRF 层 计算loss
            log_likehood,self.trans = crf.crf_log_likelihood(
                inputs = logits,
                tag_indices=targets,
                transition_params=self.trans,
                sequence_lengths=lengths
            )
            return -tf.reduce_mean(log_likehood)

    def run_step(self,sess,batch,is_train=True):
            feed_dict = {self.char_inputs: batch[0],
                         self.targets: batch[1],
                         # self.bound_inputs: batch[2],
                         # self.flag_inputs: batch[3],
                         # self.radical_inputs: batch[4],
                         # self.pinyin_inputs: batch[5],
                         }
            if is_train:
                global_step,train_loss,_ = sess.run([self.global_step,self.cost, self.train_op], feed_dict=feed_dict)
                return global_step,train_loss
            else:
                # feed_dict.pop(self.targets)
                logits,length = sess.run([self.logits,self.length], feed_dict=feed_dict)
                return logits,length

    def decode(self, logits, lengths, matrix):
        """使用维特比（viterbi）解码
        :param logits: [batch_size, num_steps, num_tags]float32, logits
        :param lengths: [batch_size]int32, real length of each sequence
        :param matrix: transaction matrix for inference
        :return:
        """
        paths = []
        small = -1000.0
        start = np.asarray([[small] * self.num_tags + [0]])
        for score, length in zip(logits, lengths):
            score = score[:length] # 使用真实句子长度
            pad = small * np.ones([length, 1])
            logits = np.concatenate([score, pad], axis=1)
            logits = np.concatenate([start, logits], axis=0)
            path, _ = crf.viterbi_decode(logits, matrix)
            paths.append(path[1:])
        return paths

    def predict(self,sess,batch,txt_content=None):
        matrix = self.trans.eval()
        logits,lengths = self.run_step(sess,batch,is_train=False)
        paths = self.decode(logits,lengths,matrix)
        chars = batch[0]
        targets = batch[1]
        results = []
        for i in range(len(paths)):
            length = lengths[i]
            if txt_content is None:
                string = [self.mp['word'][0][index] for index in chars[i][:length]]
            else:
                string = list(txt_content)

            real_tags = [self.mp['label'][0][index] for index in targets[i][:length]]
            predict_tags = [self.mp['label'][0][index] for index in paths[i]]
            sub_res = [list(item) for item in zip(string,real_tags,predict_tags)]
            results.extend(sub_res)
        return results

    def evaluate_line(self, sess, inputs, id_to_tag):
        trans = self.trans.eval(session=sess)
        lengths, scores = self.run_step(sess,inputs,is_train=False)
        batch_paths = self.decode(scores, lengths, trans)
        tags = [id_to_tag[idx] for idx in batch_paths[0]]
        return tags



