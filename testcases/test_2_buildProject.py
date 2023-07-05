import unittest
from library.ddt import ddt, data
from common.readexcel import ReadExcel
import os
from common.contents import DATA_DIR, RESOURCES_DIR
from common.request import HandRequests
from common.config import conf
from common.logger import my_log
import jsonpath
from common.parametric import TestData, replace_data
from common.db import HandleDB
import request
import time

@ddt
class TestBuildProject(unittest.TestCase):
    excel_path = os.path.join(DATA_DIR, "cases.xlsx")
    excel = ReadExcel(excel_path, "buildProject")
    cases = excel.read_data()
    http = HandRequests()
    db = HandleDB()

    @data(*cases)
    def test_buildProject(self, case):

        global headers_uploadFile, url_uploadFile, data_uploadFile, url, data, headers, files_uploadFile
        #上传招标文件
        if case["interface"] == "uploadFile":
            headers_uploadFile = eval(conf.get_str("env", "headers2"))
            url_uploadFile = case["url"]
            files_uploadFile = {"file": ("房建施工-简易评估法-现场.GZBS", open("D:\\HaiNanJQG\\resources\\房建施工-简易评估法-现场.GZBS", "rb"),"application/octet-stream")}
            data_uploadFile = eval(replace_data(case["data"]))
        else:
            headers = eval(conf.get_str("env", "headers"))
            url = replace_data(conf.get_str("env", "url") + case["url"])
            data = replace_data(case["data"]).encode('utf-8')

        if case["interface"] != "login":
            headers["Authorization"] = conf.get_str("params","cookie")

        method = case["method"]
        expected = eval(case["expected"])

        if case["interface"] == "uploadFile":
            response = self.http.send(headers=headers_uploadFile,method=method, url=url_uploadFile,files=files_uploadFile,data=data_uploadFile)
        else:
            response = self.http.send(headers=headers, method=method, url=url, params=data, data=data, json=data)
        print(response)
        result = response.json()

        print("接口序号：{}".format(case["case_id"]))
        print("接口名称：{}".format(case["interface"]))
        print("接口名称：{}".format(case["title"]))
        print("预期结果：{}".format(expected))
        print("实际结果：{}".format(result))

        if case["interface"]=="getUploadUrl":
            logicPath = jsonpath.jsonpath(result, "$..logicPath")[0]
            conf.write_data("params","logicPath",logicPath)
            print(logicPath)
        elif case["interface"] == "uploadFile":
            fileId = jsonpath.jsonpath(result, "$..fileId")[0]
            filePath = jsonpath.jsonpath(result, "$..filePath")[0]
            nowTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            conf.write_data("params","fileId",fileId)
            conf.write_data("params", "filePath", filePath)
            conf.write_data("params","nowTime",nowTime)
        elif case["interface"] == "createProjectByTenderFile":
            projectId = jsonpath.jsonpath(result, "$..projectId")[0]
            bidSectionId = jsonpath.jsonpath(result, "$..bidSectionId")[0]
            bidSectionCode = jsonpath.jsonpath(result, "$..bidSectionCode")[0]
            conf.write_data("params","projectId",projectId)
            conf.write_data("params", "bidSectionId", bidSectionId)
            conf.write_data("params", "bidSectionCode", bidSectionCode)
        elif case["interface"] == "projectlistToday":
            domainId = jsonpath.jsonpath(result, "$..domainId")[0]
            conf.write_data("params","domainId",domainId)

        try:
            self.assertEqual(result["code"], expected["code"])
            self.assertEqual(result["msg"], expected["msg"])
        except AssertionError as e:
            self.excel.write_data(row=case["case_id"] + 1, column=9, value="不通过")
            my_log.info("用例：{}执行未通过".format(case["title"]))
            my_log.error(e)
            my_log.exception(e)
            raise e
        else:
            self.excel.write_data(row=case["case_id"] + 1, column=9, value="通过")
            my_log.info("用例：{}执行通过".format(case["title"]))


if __name__ == '__main__':
    unittest.main()
