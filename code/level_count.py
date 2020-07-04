# *- coding: utf-8 -*-
# @Author: bruce li
# @Date:   2019-01-10 19:22:29
# @Last Modified by:  bruce li
# @Last Modified time: 2019-02-26 17:55:02
# @Email:	talkwithh@163.com
#统计类目信息
import os
from read_write_tool import read_file

def merge_level3(file_path,fp):
	for level in os.listdir(file_path):
		if '.txt' in level:
			continue
		for file in os.listdir(file_path+level+'/'):
			if 'count' in file:
				continue
			con = read_file(file_path+level+'/'+file,'utf-8')
			fp.write(con)

def count_level1(file_path):
	level_dic = {}
	level1_count = 0
	for level in os.listdir(file_path):
		if '.txt' in level:
			continue
		temp_count = 0
		level_dic[level] = []
		for file in os.listdir(file_path+level+'/'):
			if 'count' in file:
				con = read_file(file_path+level+'/'+file,'utf-8').split('\n')
				level1_count += len(con)-2
				level_dic[level].append(len(con)-2)

				for i in con[:-2]:
					num = i.split('-->')[1]
					temp_count += int(num[:-1])
				level_dic[level].append(temp_count)
				print(str(len(con)-2)+'/'+str(temp_count))
	print(str(level_dic))
	print(level1_count)

def get_level3_name(file_path,save_path):
	level3_dic = {}
	
	t = open(save_path,'a',encoding='utf-8')
	for level in os.listdir(file_path):
		if '.txt' in level:
			continue
		level3_dic[level] = []
		for file in os.listdir(file_path+level+'/'):
			if 'count' in file:
				con = read_file(file_path+level+'/'+file,'utf-8').split('\n')
				for i in con[:-2]:
					level3 = i.split('-->')[0]
					t.write(level3+'\n')
					print(level3)
					level3_dic[level].append(level3)
	print(level3_dic)

if __name__ == '__main__':
	file_path = '../datas/data_set/train/'
	file_path2 = '../datas/data_set/test/'
	save_path = '../datas/data_set/level_3_new/'
	count_level1(file_path)
	level3_count_save = '../datas/data_set/level3_name.txt'
	# get_level3_name(file_path,level3_count_save)

	new_train_save = save_path+'train'+'/'
	new_test_save = save_path+'test'+'/'
	if not os.path.exists(new_train_save):
		os.makedirs(new_train_save)
	if not os.path.exists(new_test_save):
		os.makedirs(new_test_save)
	train_fp = open(new_train_save+'level_3_train.txt','a',encoding='utf-8')
	test_fp = open(new_test_save+'level_3_test.txt','a',encoding='utf-8')

	# merge_level3(file_path,train_fp)
	# merge_level3(file_path2,test_fp)

