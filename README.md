# text-classify
Classification of journal data(期刊数据分类)


# 前言
本程序实现了对没有标注中图分类号的期刊数据自动标引上中图分类号（三级）。
训练模型使用的数据集规模为，包括22个大类，1190左右三级类。数据集的内容、规模和类别数据量分布等对训练过程会产生一定影响。
训练时有两个模型：
1.类目标签993个。剔除了三级类目的数据数量少于200的类目，请见文档text_classifier\datas\data_set\train_count2.txt。
2.类目标签620个。剔除了三级类目的数据数量少于1000的类目，请见文档text_classifier\datas\data_set\train_count.txt。
训练准确率：
模型1(类目993):0.68
模型2(类目620):0.96


# 项目文件目录结构
+--code
|      +--prediction.py
|      +--load_model.py
+--datas
|      +--data_set
|      +--inputfiles
|      +--model
|      +--results
+--description.txt
+--tool
+--linux_path.txt
+--windows_path.txt

# 项目程序使用说明
python版本：python3.6.0
prediction.py---预测文件主程序
load_model.py---加载模型程序

## 安装包
控制台输入：
pip install jieba
安装fasttext包：
windows环境,fasttext包路径在tool文件夹下：
pip install fasttext-0.8.22-cp36-cp36m-win_amd64.whl
linux环境
pip install fasttext



## 使用说明
(1)	在'path.txt'中设置待预测的文本的绝对路径，如：
	预测文件绝对路径：
	C:\Users\bruce\Desktop\text_classifier\datas\inputfiles\
	
	在设置的路径中放入待预测的文本
	格式：'.txt'
	内容：中文。一段或一篇文字。

(2)	在'path.txt'中设置预测结果保存的绝对路径，如：
	预测结果保存绝对路径：--此行不可修改
	C:\Users\bruce\Desktop\text_classifier\datas\results\
(3) 	在'path.txt'中设置预测模型选择路径，cate=990表示可分990个类标签的分类器。如：
	预测模型选择路径：--此行不可修改
	C:\Users\bruce\Desktop\text_classifier\datas\model\cate=990\
(4)	打开控制台，进入'text_classifier/code'路径
	输入'python prediction.pyc' 回车运行！


## 运行结果说明
程序运行结果形式为文件名+预测的三个类名，概率形式给出(概率从大到小)
如：文本：10.txt-->
	预测类别：['TB4', 'TQ32', 'TM4']
	概率：[ 0.06224982  0.04323245  0.03611365]
结果保存在'../datas/results/_pre_results.txt'


# 版本更新说明
训练模型更新主要依赖于数据文件中model文件夹中的fastText_classifier.model文件
