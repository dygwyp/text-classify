#coding='utf-8'
#读写文件的函数，包括bunch对象的读写
'''
@author: brunce.li
E-mail: 2471249566@qq.com
'''

import pickle
import codecs
#import chardet
from sklearn.externals import joblib

def save_file(savepath, content,way):
    with codecs.open(savepath, way,encoding='utf8') as fp:
        fp.write(content)
        fp.write('\n')

def read_file(path,way):
    '''
    #判断文件编码类型
    with codecs.open(path,'rb') as fp:
        con = fp.read()
        result = chardet.detect(con)
    '''
    with codecs.open(path, "r+",way) as fp:
        content = fp.read()
    return content

def writebunch_obj(path, bunchobj):
    with codecs.open(path, "wb") as file_obj:
        pickle.dump(bunchobj, file_obj)

def readbunch_obj(path):
    with codecs.open(path, "rb") as file_obj:
        bunch = pickle.load(file_obj)
    return bunch

def save_model(model,model_path):
    joblib.dump(model, model_path)

def load_model(model_path):
    return joblib.load(model_path)
