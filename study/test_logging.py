#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@Time    :    2021/4/21 0021 6:01
#@Author  :    tb_youth
#@FileName:    test_logging.py
#@SoftWare:    PyCharm
#@Blog    :    https://blog.csdn.net/tb_youth


import logging
from logging import handlers


class TestLogger(object):
    '''Level
    CRITICAL : 50
    ERROR : 40
    WARNING :30
    INFO : 20
    DEBUG : 10
    NOTSET :0
    '''
    def logger_in_console(self):
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        logger.info('This is logger info.') # 不显示，因为Level默认为Warning
        logging.debug('This is logger debug') # 同上
        # 即只有>=level的log才会显示
        logger.warning('This is logger warning.')
        logger.error('This is logger error.')
        logger.critical('This is logger critical.')
        # logger.setLevel(logging.DEBUG)
        fmt = logging.Formatter('[%(asctime)s - %(filename)s - %(name)s - %(levelname)s] - %(message)s')
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(fmt)
        console_handler.setLevel(logging.INFO)
        logger.addHandler(console_handler)
        logger.info('This is logger info.')
        logger.warning('This is logger warning.')
        logger.error('This is logger error.')
        logger.critical('This is logger critical.')
        pass



    def logger_in_file(self):
        # logging.basicConfig(filename='example.log',encoding='utf-8',level=logging.DEBUG)
        logger = logging.getLogger(__name__) # user 'name = __name__' is a good way
        file_log_path = './example.log'
        file_handler = logging.FileHandler(file_log_path, encoding='utf-8')
        dtfmt = '%m/%d/%Y %I:%M:%S %p'
        fmt = logging.Formatter('[%(asctime)s - %(filename)s - %(name)s - %(levelname)s] - %(message)s',datefmt=dtfmt)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(fmt,)
        logger.addHandler(file_handler)
        logger.debug('This is logger debug writed in {}'.format(file_log_path))
        logger.info('Good Night!')

    def mg(self):
        logger = logging.getLogger(__name__)
        logger.info('This is logger info.')  # 不显示，因为Level默认为Warning
        logger.warning('This is logger warning.')
        logger.error('This is logger error.')
        logger.critical('This is logger critical.')
        logger.setLevel(logging.DEBUG)
        fmt = logging.Formatter('[%(asctime)s - %(filename)s - %(name)s - %(levelname)s] - %(message)s')
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(fmt)
        console_handler.setLevel(logging.INFO)
        logger.addHandler(console_handler)
        logger.info('This is logger info.')
        logger.warning('This is logger warning.')
        logger.error('This is logger error.')
        logger.critical('This is logger critical.')
        file_log_path = './example1.log'
        file_handler = logging.FileHandler(file_log_path, encoding='utf-8',mode='w') # default  value of mode is 'a'
        dtfmt = '%m/%d/%Y %I:%M:%S %p'
        fmt = logging.Formatter('[%(asctime)s - %(filename)s - %(name)s - %(levelname)s] - %(message)s', datefmt=dtfmt)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(fmt, )
        logger.addHandler(file_handler)
        logger.debug('This is logger debug writed in {}'.format(file_log_path))
        logger.info('Good Night!')

    def test_handler(self):
        # 间隔(interval)15天（d）,除你指定的文件外，之后最多保存6个文件（即共7个log文件），多了删除最旧
        handlers.TimedRotatingFileHandler(filename='./default.log', when='d', interval=15, backupCount=6,
                                          encoding='utf-8', delay=False, utc=False, atTime=None)
        # 每个文件（maxBytes=10240bytes）最大10kb，超过这个数值时，就创建一个新的文件，backupCount=6同上
        handlers.RotatingFileHandler(filename='./default.log', mode='a', maxBytes=10240, backupCount=6, encoding=None, delay=False)

def test_logger():
    tg = TestLogger()
    tg.logger_in_console()
    # tg.logger_in_file()
    # tg.mg()


if __name__ == '__main__':
    pass