# *- coding: utf-8 -*-
# @Author: bruce li
# @Date:   2019-01-22 10:39:39
# @Last Modified by:  bruce li
# @Last Modified time: 2019-01-22 15:44:57
# @Email:	talkwithh@163.com
#划分数据集为训练集和测试集、

import os,sys
from read_write_tool import read_file

def div_train_test(file_path,train_path,test_path):
	if not os.path.exists(train_path):
		os.makedirs(train_path)
	if not os.path.exists(test_path):
	    os.makedirs(test_path)
	lev1 = os.listdir(file_path)

	for l1 in lev1:
		if '.txt' in l1:
			continue
		if len(os.listdir(file_path+l1+'/')) == 0:
			continue
		file = file_path+l1+'/'+l1+'_train.txt'
		count_file = file_path+l1+'/'+l1+'_train_count.txt'

		save_train_path = train_path+l1+'/'
		save_test_path = test_path+l1+'/'
		
		if not os.path.exists(save_train_path):
			os.makedirs(save_train_path)
		if not os.path.exists(save_test_path):
			os.makedirs(save_test_path)

		save_train_file = save_train_path+l1+'_train.txt'
		save_test_file = save_test_path+l1+'_test.txt'
		save_tr_count = save_train_path+l1+'_train_count.txt'
		save_te_count = save_test_path+l1+'_test_count.txt'

		train_fp = open(save_train_file,'w',encoding='utf-8')
		train_count_fp = open(save_tr_count,'w',encoding='utf-8')
		test_fp = open(save_test_file,'w',encoding='utf-8')
		test_count_fp = open(save_te_count,'w',encoding='utf-8')

		con = read_file(file,'utf-8').split('\n')
		count_con = read_file(count_file,'utf-8').split('\n')

		lev3_test_dic = {}
		#统计三级类数目，确定划分比例
		for l3 in count_con[:-2]:
			le3_count = l3.split('-->')
			num = le3_count[1].replace(',','')
			test_num = int(num)/5		#按照4：1划分数据集
			train_num = int(int(num)-int(test_num))
			lev3_test_dic[le3_count[0]] = int(test_num)	
			train_count_fp.write(le3_count[0]+'-->'+str(train_num)+'\n')
			test_count_fp.write(le3_count[0]+'-->'+str(int(test_num))+'\n')
		
		# print(lev3_test_dic)
		train_count_fp.write(str(count_con[-2]))
		test_count_fp.write(str(count_con[-2]))

		temp_test_count = 0
		temp_label = list(lev3_test_dic.keys())[0]
		for act in con[:-1]:
			row = act.split(',')
			label = row[0].split('__')[-1]

			test_count = lev3_test_dic[label]
			if label == temp_label:
				if temp_test_count <= test_count:
					test_fp.write(act)
				else:
					train_fp.write(act)
				temp_label = label
				temp_test_count += 1
			else:
				temp_test_count = 1
				train_fp.write(act)
				temp_label = label
		# break

if __name__ == '__main__':
	file_path = '../datas/data_set/train/'
	train_path = '../datas/data_set/train2/'
	test_path = '../datas/data_set/test2/'
	div_train_test(file_path,train_path,test_path)