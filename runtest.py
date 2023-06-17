import unittest

from library.HTMLTestRunnerNew import HTMLTestRunner

from common.readexcel import ReadExcel
from common.contents import TESTCASES_DIR
from common.contents import REPORT_DIR
from common.config import conf
import os


#第一步：创建一个测试套件
suite=unittest.TestSuite()

#第二步：将测试用例，加载到测试套件中
#创建加载对象
loader=unittest.TestLoader()

#1）以模块为单位
# suite.addTest(loader.loadTestsFromModule(testcases))

#2)以类为单位
# suite.addTest(loader.loadTestsFromTestCase(testcases.LoginTestCase))

#3)以用例为单位
#创建一个实例对象，通过用例类去创建测试用例对象的时候，需要传入用例的方法名（字符串类型）
# excle=ReadExcel("cases.xlsx","login")
# cases=excle.read_data()
#
# for i in cases:
#     case=LoginTestCase("test_login",eval(i["data"]),eval(i["expected"]),i["case_id"])
#     suite.addTest(case)

#4）以路径为单位
# suite.addTest(loader.discover(r"用例文件所在的路径"))
suite.addTest(loader.discover(TESTCASES_DIR))

#第三步：创建一个测试运行程序启动器
#runner=unittest.TextTestRunner()
#或者
filename=conf.get_str("report","filename")
report_path=os.path.join(REPORT_DIR,filename)

runner=HTMLTestRunner(stream=open(report_path,"wb"),   #打开一个报告文件，将句柄传给stream，wb覆盖写入模式
                                          tester="yuxx",   #报告中显示的测试人员
                                          description="报告的描述信息",   #报告中显示的描述信息
                                          title="海南机器管_接口自动化测试报告")   #报告的标题

#第四步：使用启动器去执行测试套件
runner.run(suite)

