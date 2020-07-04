# -*- coding: utf-8 -*-
"""
寻找分类精度最大的类别数目
@author: bruce
"""

import os,re
import time
import fastText.FastText as ff
from read_write_tool import read_file

#训练分类模型
def fastText_classifier(marge_train_path,train_data,model_save_path,result_save_path):
    files_list = []
    results = []

    if not os.path.exists(marge_train_path):
    	os.makedirs(marge_train_path)

    for root,dirs,files in os.walk(train_data,topdown=False):
    	for file in files:
    		files_list.append(os.path.join(root,file))

    marge_files(files_list,marge_train_path,2)
    '''
    for data_file in os.listdir(train_data):
        if os.path.isdir(train_data+data_file):
            print(data_file)
            file = os.listdir(train_data+data_file)
            if len(file) == 0:
                continue
            classifier=ff.train_supervised(train_data+data_file+'/'+file[0],lr=0.1,loss='hs',wordNgrams=2,epoch=100)
            # classifier = load_model.load_model(model_save_path+'train_'+data_file+'_classifier.model','nt')         
            model = classifier.save_model(model_save_path+'train_'+data_file+'_classifier.model') # 保存模型
            classifier.get_labels() # 输出标签
            result = classifier.test(train_data+data_file+'/'+file[0])
            files.append(data_file)
            results.append(result)
            print(result)
       
    print(files)
    print(results)

    write_results(result_save_path)
	'''

#合并三级类
def marge_files(train_files_path,marge_path,block_num):
	level_3_nums = []
	marge_file_list = []
	train_files_path = train_files_path[0:-1]
	files_path = train_files_path[0::2]
	count_path = train_files_path[1::2]
	#获得类目数量	
	for path in count_path:
		con = read_file(path,'utf-8').split(',')
		num = con[-2].split('-->')[1]
		level_3_nums.append(int(num))
	#定义文件和类目数量字典
	file_count_dic = dict(zip(files_path,level_3_nums))
	#获得合并列表
	for i in range(block_num,len(files_path),block_num):
		marge_file_list.append(files_path[0:i])
	marge_file_list.append(files_path)
	c = 0
	for item in marge_file_list:
		nums = 0
		c += block_num
		for i in item:
			nums += file_count_dic[i]
		write_fp = open(marge_path+str(c)+'--'+str(nums)+'.txt','a')
		for i in item:
			cons = read_file(i,'utf-8')
			write_fp.write(cons+'\n')

#保存结果
def write_results(result_save_path):
	with open(result_save_path+'train/train_results_2.txt','w') as fp:
		for i,j in zip(files,results):
			fp.write(str(i)+'-->'+str(j))
			fp.write('\n')

if __name__ == '__main__':
	marge_train_path = '../datas/data_set/merge_train/'
	train_path = '../datas/data_set/train/'
	model_save_path = '../datas/model/'
	result_save_path = '../datas/results/'
	fastText_classifier(marge_train_path,train_path,model_save_path,result_save_path)