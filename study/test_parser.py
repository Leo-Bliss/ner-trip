#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@Time    :    2021/4/21 0021 12:15
#@Author  :    tb_youth
#@FileName:    test_parser.py
#@SoftWare:    PyCharm
#@Blog    :    https://blog.csdn.net/tb_youth


import argparse


def main():
    parser = argparse.ArgumentParser(description='Test argparse') # for help will show
    parser.add_argument('-n','--name',type=str,default='Lai',help='input your name')
    parser.add_argument('-y','--year',type=int,default=2021,help='input your last year in your university')
    args = parser.parse_args()
    print(args)
    print('name = ',args.name)
    print('year = ',args.year)


if __name__ == '__main__':
    main()

