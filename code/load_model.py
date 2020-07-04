# -*- coding: utf-8 -*-
"""
加载模型接口
@author: bruce
""" 

def load_model(model_path):
	#加载模型
    #加载windows模型
	import fastText.FastText as ff
	classifier = ff.load_model(model_path)
	return classifier