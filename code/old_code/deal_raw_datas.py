# -*- coding: utf-8 -*-
"""
处理原始数据，生成训练数据集
@author: bruce
"""
import os,re
import time
import random
# import fasttext
import jieba
import codecs
import pandas as pd
from read_write_tool import read_file,save_file
        
# 抽取n级类目
def con_to_levn(con,ori_datas_path,le_path_list,save_path,class_info,title_n):
    '''
    param ori_datas_path:txt文件,索引为id、标题、关键词、摘要、中图分类号、母体文献
    param le_path_list:层级目录文件
    param save_path:标注的数据集存储路径
    param class_info:输入层级
    param title_n:抽取的标题重复次数
    output:标注好的分类文件夹，每个文件夹代表一个n级类别，类别中有多个文本数据。
    '''
    train_path = save_path+'train/'
    test_path = save_path+'test/'
    if not os.path.exists(train_path):
        os.makedirs(train_path)
    if not os.path.exists(test_path):
        os.makedirs(test_path)

    
    #读取数据
    # con = read_datas(ori_datas_path)
    # 
    levs = []
    levs_area = list(con['区域分类'])
    levs_industry = list(con['行业分类'])
    levs_subject = list(con['学科分类'])
    for i in range(len(levs_subject)):
        levs_subject[i] = str(levs_subject[i])
    levs_china_class = list(con['中图分类'])

    levs.append(levs_area)
    levs.append(levs_industry)
    levs.append(levs_subject)
    levs.append(levs_china_class)

    classes = list(class_info.keys())
    lens = list(class_info.values())

    for i in range(len(le_path_list)):    
        # 读取层级目录
        start2 = time.time()
        read_Ch_cate(save_path,le_path_list[i],classes[i],lens[i])
        le_n_names = read_file(save_path+'level_'+classes[i]+'_'+str(lens[i])+'.txt','utf-8').split(',')
        # 抽取n级目录数据
        select_txt(classes[i],con,le_n_names,levs[i],train_path+classes[i],test_path,stopword_path,lens[i])
        end2 = time.time()
        run_slect_time = round(end2-start2,3)
        print('生成数据集运行时间：'+str(run_slect_time)+'s')
        # break
    
#读取数据
def read_datas(ori_datas_path):
    print('读取原始数据...')
    # try:
    #     t = open(ori_datas_path,encoding='utf-8')
    # except:
    #     t = open(ori_datas_path,encoding='gbk')     
    con = pd.DataFrame(pd.read_excel(ori_datas_path,encoding="utf-8"))
    con = con.fillna(value='')
    # print(con.head())
    return con

# 读取中图分类号
def read_Ch_cate(save_path,le_file_path,class_info,len_info):
    print('读取中图分类号...')
    if not '.txt' in os.listdir(save_path):
        infos = pd.read_excel(le_file_path)
        #抽取n级类号数据
        le_n_datas = infos.loc[infos['层级']==int(len_info)]
        le_n_id = list(le_n_datas['类号ID'])
        
        le_select = []
        for i in le_n_id:
            if i not in le_select:
                # i = re.sub(r'[\r\n\t]','',i)
                le_select.append(str(i))

        #存储n级目录
        save_file(save_path+'level_'+class_info+'_'+str(len_info)+'.txt',','.join(le_select),'w')

#抽取文本
def select_txt(le_n,con,le_n_names,levs,train_path,test_path,stopword_path,lens):
    print('抽取数据,生成训练和测试数据集...')
    #分类的类别数量
    cate_count = 0
    #临时数据保存
    train_list = []
    test_list = []
    stopword = read_file(stopword_path,'utf').split('\n')
    for i in le_n_names:    #n级目录列表
        #类别数据个数统计
        count_train = 0
        count_test = 0
        #临时保存数据
        test = []
        train = []
        #训练文件集一级类名字
        # le1_name = i[0]
        len_num = 1
        
        if '/' in i:
            i=i.replace(r'/',' ')

        for j in enumerate(levs[:]): #原始数据分类号列表

            j_list=[]
            try:
                if ';' in j[1]:    #类别数大于1时
                    j_list = j[1].split(';')   
                else:
                    j_list.append(j[1])
            except:
                continue          
            for p in j_list:  
                p=str(p)  
                #print(p[0])
                if len(p) == 0:
                    continue
                # elif i[0] == p[0] and i in p: #符合n级目录则抽取
                elif len(i) >= 3 and len(p) >= 3 and i[:3] == p[:3]: #符合n级目录则抽取
                    index = j[0]   #获得待抽取数据索引
                    item = con.loc[index]
                    # title = item['标题']   #抽取数据标题
                    content = item['ContentText']  #抽取数据摘要，作为文本内容
                    # key_word = item['关键词'] #抽取数据关键词
                    # content = title+' '+content+' '+key_word
                    try:
                        # if len_num%8==0:
                        #     test.append(deal_datas(i,content,stopword))
                        #     count_test+=1
                        # else:
                        train.append(deal_datas(i,content,stopword))
                        count_train+=1
                    except:
                        print('抽取数据类别%s时出错！'%i)
                    else:
                        len_num+=1
        
        if count_train >= 20 :
            save_file(train_path+'train_'+lens+'_count.txt',i+'-->'+str(count_train)+',','a')
            train_list.append(train)
            cate_count += 1
        # if count_test >= 0:
        #     save_file(test_path+'test_'+lens+'_count.txt',i+'-->'+str(count_test)+',','a')
        #     test_list.append(test)

    #打乱数据，使得同类别的样本不至于扎堆
    for l1 in test_list:
        random.shuffle(l1)
        write_datas(test_path+'level_'+lens+'_test.txt',l1)
    for l2 in train_list:
        random.shuffle(l2)
        write_datas(train_path+'level_'+lens+'_train.txt',l2)
    
    save_file(train_path+'train_'+lens+'_count.txt','类别数目: '+str(cate_count)+',','a')

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
    # le_n = input('请输入分类层级号：(1,2,3)')

    class_info = {'区域分类':'3','行业分类':'3','学科分类':'2','中图分类':'3'}
    class_info_book = {'区域分类':'1','行业分类':'1','学科分类':'1','中图分类':'1'}

    stopword_path = '../datas/data_set/stopwords/中文.txt'
    ori_path0 = '../datas/data_set/original_datas/book.xlsx'
    ori_path1 = '../datas/data_set/original_datas/part1.xlsx'
    ori_path2 = '../datas/data_set/original_datas/part2.xlsx'
    ori_path3 = '../datas/data_set/original_datas/part3.xlsx'
    ori_path4 = '../datas/data_set/original_datas/part4.xlsx'

    le_path_list = []
    le_add_path = '../datas/data_set/category/区域分类.xlsx'
    le_ind_path = '../datas/data_set/category/行业分类.xlsx'
    le_sub_path = '../datas/data_set/category/学科分类.xlsx'
    le_ch_path = '../datas/data_set/category/classify_list.xlsx'

    le_path_list.append(le_add_path)
    le_path_list.append(le_ind_path)
    le_path_list.append(le_sub_path)
    le_path_list.append(le_ch_path)

    save_path = '../datas/data_set/input_datas_2/'

    con0 = read_datas(ori_path0)
    # con1 = read_datas(ori_path1)
    # con2 = read_datas(ori_path2)
    # con3 = read_datas(ori_path3)
    # con4 = read_datas(ori_path4)
    
    # re1 = con1.append(con2,ignore_index=True)
    # re2 = con3.append(con4,ignore_index=True)
    # re = re1.append(re2,ignore_index=True)

    con_to_levn(con0,ori_path1,le_path_list,save_path,class_info_book,stopword_path)
