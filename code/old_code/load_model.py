# -*- coding: utf-8 -*-
"""
加载模型接口
@author: bruce
""" 

def load_model(model_path,os_name):
	#加载模型
    #加载windows模型
	if os_name == 'nt':
		import fastText.FastText as ff
		classifier = ff.load_model(model_path)
	else:    #加载linux模型
		import fasttext
		classifier = fasttext.load_model(model_path, label_prefix='__label__')

	return classifier