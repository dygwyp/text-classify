 # -*- coding: utf-8 -*-
'''
预测代码接口
@author:bruce
测试分层分类器，未加入优化算法
'''
import os,re,time
import jieba
import load_model

def prediction(test_data_path,model_save_path,result_save_path,level3_name,stopword_path):
	start = time.time()
	#读取停用词
	stopword = read_file(stopword_path,'utf-8').split('\n')
	models = os.listdir(model_save_path)
	#获得测试集文件列表
	test_files = get_test_files_path(test_data_path)
	# print(test_files)

	#获得3级类名
	level3_list = read_file(level3_name,'utf-8').split('\n')

	#加载第一层级分类器
	classifier = load_model.load_model(model_save_path+'level_1_train.txt_classifier.model')
	end = time.time()
	print('加载第一层级模型用时%.2f'%(end-start))
	#一层级预测文件
	_pre_result_ = {}
	all_count = 0
	all_right_count = 0
	for file in test_files:
		right_label = []
		right_con = []
		if 'count' in file or 'level' in file:
			continue
		right_count = 0
		text_list = []
		texts = read_file(file,'utf-8')
		label_list,con_list = deal_datas(texts)
		all_count += len(label_list)
		for label,con in zip(label_list,con_list):		
			pre_label = classifier.predict(con,k=3)
			_label_ = pre_label[0][0][0].replace(',','')
			_pro_ = pre_label[1][0][0]
			if _label_ in label:
				right_count += 1
				right_label.append(label)
				right_con.append(con)
			# print(_label_+'--'+label)
			# print(_pro_)
			_pre_result_[str(pre_label)] = label
		print(file+' one_level_pre:'+str(right_count/len(label_list)))

		flag,three_right_count = 0,0
		for i,j in zip(right_label,right_con):
			l = i.split('__')[-1]
			for model in models:
				if l[0] in model and not flag:
					classifier_three = load_model.load_model(model_save_path+model)
					flag = 1
			if flag:
				if not l in level3_list:
					three_right_count += 1
					all_right_count += 1
				pre_label_three = classifier_three.predict(j,k=3)
				_label_three = pre_label_three[0][0][0].replace(',','')
				_pro_three = pre_label_three[1][0][0]

				if _label_three == i:
					three_right_count += 1
					all_right_count += 1
					# print(_label_three+'--'+i)
					# print(_pro_three)
		print(file+' three_level_pre:'+str(three_right_count/len(label_list)))
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
	labels = []
	con_list = []
	cons = content.split('\n')
	for data in cons:
		if len(data) == 0:
			continue
		d = data.split(',')
		label = d[0]
		labels.append(label)
		con_list.append([d[1]])

	return labels,con_list

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
	test_data_path = '../datas/data_set/test3/'
	model_save_path = '../datas/model/paper_train/'
	result_save_path = '../datas/results/test/'
	level3_name = '../datas/data_set/level3_name.txt'
	stopword_path = '../datas/infos/stopwords/中文.txt'

	prediction(test_data_path,model_save_path,result_save_path,level3_name,stopword_path)