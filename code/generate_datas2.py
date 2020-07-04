# -*- coding: utf-8 -*-
"""
处理原始数据，生成训练数据集
@author: bruce
"""
import os,re
import time
import random
import jieba
import pandas as pd
import fastText.FastText as ff
from read_write_tool import read_file,save_file
        
# 抽取n级类目
def con_to_levn(ori_datas_path,le_file_path,save_path,stopword_path):
    '''
    param ori_datas_path:txt文件,索引为id、标题、关键词、摘要、中图分类号、母体文献
    param le_file_path:层级目录文件
    param save_path:标注的数据集存储路径
    param le_n:输入层级
    param title_n:抽取的标题重复次数
    param stopword_path:停用词路径
    output:标注好的分类文件夹，每个文件夹代表一个n级类别，类别中有多个文本数据。
    '''
    train_path = save_path+'train/'
    test_path = save_path+'test/'
    if not os.path.exists(train_path):
        os.makedirs(train_path)
    if not os.path.exists(test_path):
        os.makedirs(test_path)

    start2 = time.time()
    #读取数据
    con = read_datas(ori_datas_path)
    levs = list(con['中图分类号'])
    
    # 读取层级目录
    le_n = ['1','3']
    #读取1级目录
    read_Ch_cate(save_path,le_file_path,le_n[0])
    le_1_names = read_file(save_path+'level_'+str(le_n[0])+'.txt','utf-8').split(',')
    #读取3级目录
    read_Ch_cate(save_path,le_file_path,le_n[1])
    le_3_names = read_file(save_path+'level_'+str(le_n[1])+'.txt','utf-8').split(',')

    # 抽取n级目录数据 
    select_txt(le_n,con,le_3_names,levs,train_path,test_path,stopword_path)
    end2 = time.time()
    run_slect_time = round(end2-start2,3)
    print('生成数据集运行时间：'+str(run_slect_time)+'s')
    
#读取数据
def read_datas(ori_datas_path):
    print('读取原始数据...')
    t = open(ori_datas_path,encoding='utf-8')
    con = pd.DataFrame(pd.read_table(t,error_bad_lines=False))
    con = con.fillna(value='')

    return con

# 读取中图分类号
def read_Ch_cate(save_path,le_file_path,le_n):
    print('读取中图分类号...')
    if not '.txt' in os.listdir(save_path):
        infos = pd.read_excel(le_file_path)
        #抽取n级类号数据
        le_n_datas = infos.loc[infos['层级']==int(le_n)]
        le_n_id = list(le_n_datas['类号ID'])
        
        le_select = []
        for i in le_n_id:
            if i not in le_select:
                # i = re.sub(r'[\r\n\t]','',i)
                le_select.append(i)

        #存储n级目录
        save_file(save_path+'level_'+str(le_n)+'.txt',','.join(le_select),'w')

#抽取文本
def select_txt(le_n,con,le_n_names,levs,train_path,test_path,stopword_path):
    print('抽取数据,生成训练和测试数据集...')
    stopword = read_file(stopword_path,'utf').split('\n')
    #分类的类别数量
    count_train_1 = 0
    count_test_1 = 0 
    #临时数据保存
    train_list = []
    test_list = []
    #三级类数目统计
    all_le3_count = 0
    le3_count_cate = 0
    #类别标志
    temp_cate = le_n_names[0][0]

    for i in le_n_names:    #n级目录列表
        #类别数据个数统计
        count_train_3 = 0
        count_test_3 = 0
        #临时保存数据
        test_1 = []
        train_1 = []
        test_3 = []
        train_3 = []

        #训练文件集一级类名字
        le1_name = i[0]
        len_num = 1

        if '/' in i:
            i=i.replace(r'/',' ')
        
        le_3_train_path = train_path+i[0]+'/'
        le_3_test_path = test_path+i[0]+'/'

        if not os.path.exists(le_3_train_path):
            os.makedirs(le_3_train_path)
        if not os.path.exists(le_3_test_path):
            os.makedirs(le_3_test_path)

        for m in enumerate(levs[:]): #原始数据分类号列表
            m_list=[]
            try:
                if ';' in m[1]:    #类别数大于1时
                    m_list = m[1].split(';')   
               	else:
                    m_list.append(m[1])
            except:
                continue          
            for p in m_list:    
                #print(p[0])
                if len(p) == 0:
                    continue
                elif i[0] == p[0] and i in p: #符合级目录则抽取
                    index = m[0]   #获得待抽取数据索引
                    item = con.loc[index]
                    title = item['标题']   #抽取数据标题
                    content = item['摘要']  #抽取数据摘要，作为文本内容
                    key_word = item['关键词'] #抽取数据关键词
                    content = title+' '+content+' '+key_word
                    try:
                        # train_1.append(deal_datas(i[0],content,stopword))
                        # train_3.append(deal_datas(i,content,stopword))
                        count_train_3+=1
                        # if len_num%5==0:
                        #     test_1.append(deal_datas(i[0],content,stopword))
                        #     test_3.append(deal_datas(i,content,stopword))
                        #     count_test_3+=1
                        # else:
                        #     train_1.append(deal_datas(i[0],content,stopword))
                        #     train_3.append(deal_datas(i,content,stopword))
                        #     count_train_3+=1
                    except:
                        print('抽取数据类别%s时出错！'%i)
                    else:
                        len_num+=1
			
        if count_train_3 >= 0:
        	#抽取三级类训练数据集
            # save_file(le_3_train_path+i[0]+'_train_count.txt',i+'-->'+str(count_train_3)+',','a')
            # random.shuffle(train_3)
            # write_datas(le_3_train_path+i[0]+'_train.txt',train_3)
            # train_list.append(train_1)   
            
            if temp_cate == i[0]:
                le3_count_cate+=1
                all_le3_count += 1
            else:
                # save_file(train_path+temp_cate+'/'+temp_cate+'_train_count.txt','类别数目'+'-->'+str(le3_count_cate)+',','a')                           
                le3_count_cate = 1
            temp_cate = i[0]
        '''   
        if count_test_3 >= 5:
        	#抽取三级类测试数据集
            save_file(le_3_test_path+i[0]+'_test_count.txt',i+'-->'+str(count_test_3)+',','a')
            random.shuffle(test_3)
            write_datas(le_3_test_path+i[0]+'_test.txt',test_3)
            test_list.append(test_1)
            '''

    #打乱数据，使同类别的数据分散
    # for l1 in test_list:
    #     random.shuffle(l1)
    #     write_datas(test_path+'level_'+le_n[0]+'_test.txt',l1)
    # for l2 in train_list:
    #     random.shuffle(l2)
    #     write_datas(train_path+'level_'+le_n[0]+'_train.txt',l2)

    # save_file(train_path+temp_cate+'/'+temp_cate+'_train_count.txt','类别数目'+'-->'+str(le3_count_cate)+',','a')                           
    print(all_le3_count)
#预处理抽取的数据
def deal_datas(label,content,stopword):
    seg_list = []
    #分词
    segs = jieba.lcut(content)               #分词
    segs=filter(lambda x:len(x)>1,segs)    #去掉长度小于1的词
    segs=filter(lambda x:x not in stopword,segs)    #去掉停用词 
    for i in segs:
        seg_list.append(i)
    str_con = '__label__'+label+', '+' '.join(seg_list)

    return str_con

#写数据
def write_datas(save_path,con):
    # print('保存fasttext格式数据...')
    with open(save_path,'a',encoding='utf-8') as fp:
        for i in con:
            fp.write(i+'\n')

if __name__ == '__main__':
    stopword_path = '../datas/infos/stopwords/中文.txt'
    ori_path1 = '../datas/data_set/original_datas/data1000_1.txt'
    ori_path2 = '../datas/data_set/original_datas/data1000_2.txt'

    le_file_path = '../datas/infos/category/classify_list.xlsx'
    save_path = '../datas/data_set/'

    # con1 = read_datas(ori_path1)
    # con2 = read_datas(ori_path2)
    # re = con1.append(con2,ignore_index=True)

    con_to_levn(ori_path1,le_file_path,save_path,stopword_path)
    