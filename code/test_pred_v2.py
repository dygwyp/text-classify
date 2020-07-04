 # -*- coding: utf-8 -*-
'''
预测代码接口
@author:bruce
测试分层分类器，加入优化算法
'''
import os,re,time
import jieba
import load_model

def prediction(test_data_path,model_save_path,result_save_path,level3_name,stopword_path):
	
	#读取停用词
	stopword = read_file(stopword_path,'utf-8').split('\n')
	models = os.listdir(model_save_path)
	#获得测试集文件列表
	test_files = read_file(test_data_path,'utf-8').split('\n')
	

	#获得3级类名
	level3_list = read_file(level3_name,'utf-8').split('\n')

	classifier_three = {}
	#加载第一层级分类器
	start = time.time()
	classifier = load_model.load_model(model_save_path+'level_1_train.txt_classifier.model')
	end = time.time()
	print('加载第一层级模型用时%.2f'%(end-start))
	#加载第三层级分类器
	start = time.time()
	for model in models:
		if 'level' in model:
			continue
		print(model)
		classifier_three[model[0]] = load_model.load_model(model_save_path+model)
						
	end = time.time()
	print('加载第三层级模型用时%.2f'%(end-start))
	#一层级预测文件	
	k_two_way_dic = []	
	all_right_count = 0
	all_count = 0
	for file in test_files:
		if ',' not in file:
			continue
		
		label,con = deal_datas(file)
		pre_label = classifier.predict(con,k=3)
		_label_ = pre_label[0][0]
		_pro_ = pre_label[1][0]
		k_two_way_dic.append([label,con,_label_])

	flag,three_right_count = 0,0
	for item in k_two_way_dic:
		it = item[0].split('__')[-1]
		if it[0] not in classifier_three.keys():
			continue
		all_count += 1
		# print(item[0]+str(item[2]))
		temp_pro = 0.0
		temp_label = ''

		for pre_lb in item[2]:
			l = pre_lb.split('__')[-1]
			
			if l[0] in classifier_three.keys():
				pre_label_three = classifier_three[l[0]].predict(item[1],k=3)
				_label_three = pre_label_three[0][0][0].replace(',','')
				_pro_three = pre_label_three[1][0][0]
				if _pro_three > temp_pro:
					temp_pro = _pro_three
					temp_label = _label_three

		if temp_label == item[0]:
			all_right_count += 1
	print('all_pre:'+str(all_right_count/all_count))
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
		con = [d[1]]
	
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
	model_save_path = '../datas/model/paper_train5/'
	result_save_path = '../datas/results/test/'
	level3_name = '../datas/data_set/level3_name.txt'
	stopword_path = '../datas/infos/stopwords/中文.txt'

	prediction(test_data_path,model_save_path,result_save_path,level3_name,stopword_path)