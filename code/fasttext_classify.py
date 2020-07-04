# -*- coding: utf-8 -*-
"""
处理原始数据，生成训练数据集
@author: bruce
"""
import os,re
import time
import fastText.FastText as ff
from read_write_tool import read_file
 
#训练分类模型
def fastText_classifier(train_data,test_data,model_save_path,result_save_path):
    files = []
    results = []
    if not os.path.exists(train_data):
        os.makedirs(train_data)
    if not os.path.exists(model_save_path):
        os.makedirs(model_save_path)
    if not os.path.exists(result_save_path):
        os.makedirs(result_save_path)

    for level_one,test_l1 in zip(os.listdir(train_data),os.listdir(test_data)):
        print(level_one+'-->'+test_l1)

        if '.txt' in level_one and '.txt' in test_l1:
            classifier=ff.train_supervised(train_data+level_one,、lr=0.1,loss='hs',wordNgrams=2,epoch=100)
            #classifier = load_model.load_model(model_save_path+'train_level_1_classifier.model','nt')
            model = classifier.save_model(model_save_path+level_one+'_classifier.model') # 保存模型
            classifier.get_labels() # 输出标签
            result = classifier.test(test_data+test_l1)
            files.append(level_one)
            results.append(result)
            print(result)
        else:
            data_list = os.listdir(train_data+level_one+'/')
            test_list = os.listdir(test_data+test_l1+'/')
            if not len(data_list) or not len(test_data):
                continue
            classifier=ff.train_supervised(train_data+level_one+'/'+data_list[0],lr=0.1,loss='hs',wordNgrams=2,epoch=50)
            #classifier = load_model.load_model(model_save_path+'train_level_1_classifier.model','nt')
            model = classifier.save_model(model_save_path+level_one+'_classifier.model') # 保存模型
            classifier.get_labels() # 输出标签
            result = classifier.test(test_data+test_l1+'/'+test_list[0])
            files.append(data_list[0])
            results.append(result)
            print(result)
    print(files)
    print(results)

    with open(result_save_path+'train_results.txt','w') as fp:
        for i,j in zip(files,results):
            fp.write(str(i)+'-->'+str(j))
            fp.write('\n')
    '''
    #linux系统
    classifier=fasttext.supervised(train_data+'level_3_train.txt',lr=0.1,loss='hs',wordNgrams=2,epoch=100,lable_prefix='__lable__')
    model = classifier.save_model(model_save_path+'fastText_classifier.model') # 保存模型
    classifier.get_labels() # 输出标签
    result = classifier.test(train_data+'level_3_train.txt')
    print(result) 
    # print("P@1:",result.precision)    #准确率
    # print("R@2:",result.recall)    #召回率
    # print("Number of examples:",result.nexamples)    #预测错的例子
    '''
if __name__ == '__main__':
    train_path = '../datas/data_set/train/'
    test_path = '../datas/data_set/test/'
    model_save_path = '../datas/model/paper_train/'
    result_save_path = '../datas/results/paper_train/'
    fastText_classifier(train_path,test_path,model_save_path,result_save_path)
