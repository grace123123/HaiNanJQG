"""
该文件用来处理整个项目的路径
"""

import os

#当前文件的绝对路径：\
#如果把项目放在服务器上路径出现问题，就把******处的__file__换成此处的dir
# dir=os.path.abspath(__file__)
# print(dir)


#__file__:当前文件的绝对路径
print(__file__)
#dirname：获取当前文件的父级目录，******
res=os.path .dirname(__file__)
print(res)
#项目目录一般用BASEDIR来表示
BASEDIR=os.path.dirname(res)
print(BASEDIR)


#配置文件的路径
CONF_DIR=os.path.join(BASEDIR,"conf")
#用例数据的目录
DATA_DIR=os.path.join(BASEDIR,"data")
#日志文件的目录
LOG_DIR=os.path.join(BASEDIR,"log")
#测试报告的目录
REPORT_DIR=os.path.join(BASEDIR,"reports")
#测试用例文件的目录
TESTCASES_DIR=os.path.join(BASEDIR,"testcases")
#外部文件目录
RESOURCES_DIR=os.path.join(BASEDIR,"resources")

