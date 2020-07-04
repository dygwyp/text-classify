# -*- coding: utf-8 -*-
"""
处理原始数据，生成训练数据集
@author: bruce
"""
import os,re
import time
import random
# import fasttext
# import jieba
import pandas as pd
from read_write_tool import read_file,save_file


def deal_datas(cut_path,save_path):
	
	cate_counts = len(count_dic)
	for i,j in count_dic.items():
		save_file(save_path+'train_count.txt',i+':'+str(j)+',','a')
	save_file(save_path+'train_count.txt','--------类目数量：'+str(cate_counts),'a')
	random.shuffle(contents)
	write_datas(save_path+'level_3_train.txt',contents)


#写数据
def write_datas(save_path,con):
    # print('保存fasttext格式数据...')
    with open(save_path,'a',encoding='utf-8') as fp:
        for i in con:
            fp.write(i+'\n')

if __name__ == '__main__':
	cut_path = '../datas/data_set'
	save_path = '../datas/data_set/level_3/train/'
	deal_datas()

