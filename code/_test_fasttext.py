# *- coding: utf-8 -*-
# @Author: bruce li
# @Date:   2019-01-22 09:48:15
# @Last Modified by:  bruce li
# @Last Modified time: 2019-01-23 09:15:31
# @Email:	talkwithh@163.com

#训练并测试fasttext，使用测试集
#
import os
import fastText.FastText as ff
from read_write_tool import read_file

#使用fasttext训练并测试小部分数据集
def test_fasttext(train_path,test_path,model_save_path):
	classifier=ff.train_supervised(train_path+'A_train.txt',lr=0.1,loss='hs',wordNgrams=2,epoch=50)
    #classifier = load_model.load_model(model_save_path+'train_level_1_classifier.model','nt')
	model = classifier.save_model(model_save_path+'A_train_classifier2.model') # 保存模型
	classifier.get_labels() # 输出标签
	result = classifier.test(test_path+'A_test.txt')
	print(result)



if __name__ == '__main__':
	train_path = '../datas/data_set/train2/A/'
	test_path = '../datas/data_set/test2/A/'
	model_save_path = '../datas/model/'
	test_fasttext(train_path,test_path,model_save_path)