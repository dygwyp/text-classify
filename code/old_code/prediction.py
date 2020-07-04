 # -*- coding: utf-8 -*-
'''
预测代码接口
@author:bruce
'''
import os,re,time
import jieba
import load_model

def prediction(test_data_path,model_save_path,result_save_path,stopword_path,os_name):
	stopword = read_file(stopword_path,'utf-8').split('\n')
	
	start = time.time()
	for model in os.listdir(model_save_path):
		classifier = load_model.load_model(model_save_path+model,os_name)
		end = time.time()
		print('加载%s模型用时%.2f'%(model,end-start))
   
	    #预测文件
		pre_dic = {}
		for file in os.listdir(test_data_path):
			text_list = []
			texts = read_file(test_data_path+file,'utf-8')
			text_list.append(deal_datas(texts,stopword))
			label = classifier.predict(text_list,k=3)
			pre_dic[file] = label
		print(pre_dic)
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
#分词，预处理
def deal_datas(content,stopword):
	seg_list = []
	segs = jieba.lcut(content)               #分词
	segs=filter(lambda x:len(x)>1,segs)    
	segs=filter(lambda x:x not in stopword,segs)    
	for i in segs:
		seg_list.append(i)
	str_con = ' '.join(seg_list)
	return str_con
#读取文件
def read_file(path,way):
	with open(path, "r+",encoding=way) as fp:
		content = fp.read()
	return content
	
if __name__ == '__main__':
	current_path = os.path.dirname(os.getcwd())
	os_name = os.name
	model_save_path = ''
	input_file = ''
	result_save_path = ''
    #读取路径
	if os_name == 'nt':  #windows
		con = read_file(current_path+'\windows_path.txt','gbk').split('\n')
		stopword_path = current_path+'\\datas\\data_set\\stopwords\\中文.txt'  
        # model_save_path = current_path+'\\datas\\model\\'
	else:
		con = read_file(current_path+'/linux_path.txt','utf-8').split('\n')
		stopword_path = current_path+'/datas/data_set/stopwords/中文.txt'  
        # model_save_path = current_path+'/datas/model/'
	for i in range(len(con)):
		if '预测文件绝对路径' in con[i]:
			input_file = re.sub(r'\r','',con[i+1])
		if '预测结果保存绝对路径' in con[i]:
			result_save_path = re.sub(r'\r','',con[i+1])
		if '预测模型选择路径' in con[i]:
			model_save_path = re.sub(r'\r','',con[i+1])
	prediction(input_file,model_save_path,result_save_path,stopword_path,os_name)