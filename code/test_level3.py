# *- coding: utf-8 -*-
# @Author: bruce li
# @Date:   2019-01-12 14:03:34
# @Last Modified by:  bruce li
# @Last Modified time: 2019-01-21 16:05:21
# @Email:	talkwithh@163.com
#测试三级分类器

import os,re,time
import jieba
import load_model

def prediction(test_data_path,model_save_path,result_save_path,level3_name,stopword_path):
	start = time.time()
	#读取停用词
	stopword = read_file(stopword_path,'utf-8').split('\n')
	
	#获得3级类名
	level3_list = read_file(level3_name,'utf-8').split('\n')

	#加载第一层级分类器
	classifier = load_model.load_model(model_save_path+'level_3_classifier.model')
	end = time.time()
	print('加载模型用时%.2f'%(end-start))
	#读取预测文件
	test_files = read_file(test_data_path,'utf-8').split('\n')
	_pre_result_ = {}
	all_count = 0
	all_right_count = 0
	right_count = 0
	for file in test_files:
		right_label = []
		right_con = []
		if ',' not in file:
			continue
		
		text_list = []
		label,con = deal_datas(file)
		all_count += 1
			
		pre_label = classifier.predict(con,k=3)
		# print(pre_label)
		_label_ = pre_label[0][0].replace(',','')
		# _pro_ = pre_label[1][0][0]
		# print(_label_)
		# print(label)
		if _label_ in label:
			right_count += 1
			
		# print(_label_+'--'+label)
		# print(_pro_)
		_pre_result_[str(pre_label)] = label

	print('all_pre:'+str(right_count/all_count))
	# print(_pre_result_)
	
	
#获得测试集文件路径列表
def get_test_files_path(test_data_path):
	test_files = []
	for root,dirs,files in os.walk(test_data_path,topdown=False):
		for name in files:
			test_files.append(os.path.join(root,name))
	return test_files

#处理测试集
def deal_datas(content):
	label,con = '',''
	d = content.split(',')
	if len(d) == 2:
		label = d[0]
		con = d[1]
	
	return label,con

#读取文件
def read_file(path,way):
	with open(path, "r+",encoding=way) as fp:
		content = fp.read()
	return content
	
#结果保存
def save_results():
	with open(result_save_path+model+'_pre_result.txt','w',encoding='utf-8') as fp:
			for i,j in pre_dic.items():
				fp.write('原文件'+i+'-->'+'\n')
				labels = []
				for p in j[0][0]:
					p = p.replace('__label__','')
					p = p.replace(',','')
					labels.append(p)
				fp.write('预测结果：'+str(labels)+'\n'+'预测标签概率'+str(j[1][0]))
				fp.write('\n')

if __name__ == '__main__':
	test_data_path = '../datas/data_set/level_3_new/test/level_3_test.txt'
	model_save_path = '../datas/model/level3_train/'
	result_save_path = '../datas/results/level_3_new/test/'
	level3_name = '../datas/data_set/level3_name.txt'
	stopword_path = '../datas/infos/stopwords/中文.txt'

	prediction(test_data_path,model_save_path,result_save_path,level3_name,stopword_path)