import unittest

import pytest

from library.ddt import ddt, data
from common.readexcel import ReadExcel
import os
from common.contents import DATA_DIR
from common.request import HandRequests
from common.config import conf
from common.logger import my_log
import jsonpath
from common.parametric import TestData, replace_data
from common.db import HandleDB


@ddt
class TestAuxiliaryTools(unittest.TestCase):
    excel_path = os.path.join(DATA_DIR, "cases.xlsx")
    excel = ReadExcel(excel_path, "auxiliaryTools")
    cases = excel.read_data()
    http = HandRequests()
    db = HandleDB()

    @data(*cases)
    def test_auxiliaryTools(self, case):

        # 上传控制价文件
        global headers_uploadFileControl, url_uploadFileControl, files_uploadFileControl, data_uploadFileControl, url, headers
        if case["interface"] == "uploadFileControl":
            headers_uploadFileControl = eval(conf.get_str("env", "headers1"))
            url_uploadFileControl = case["url"]
            files_uploadFileControl = {
                "file": ("控制价.kzj", open("D:\\HaiNanJQG\\resources\\控制价.kzj", "rb"), "application/octet-stream")}
            data_uploadFileControl = eval(replace_data(case["data"]))

        else:
            headers = eval(conf.get_str("env", "headers"))
            url = replace_data(conf.get_str("env", "url") + case["url"])
            data = replace_data(case["data"]).encode('utf-8')

        if case["interface"] != "login":
            headers["Authorization"] = conf.get_str("params", "cookie")

        method = case["method"]
        expected = eval(case["expected"])

        if case["interface"] == "uploadFileControl":
            response = self.http.send(headers=headers_uploadFileControl, method=method, url=url_uploadFileControl,
                                      files=files_uploadFileControl, data=data_uploadFileControl)
        else:
            response = self.http.send(headers=headers, method=method, url=url, params=data, data=data, json=data)
        result = response.json()
        print("接口序号：{}".format(case["case_id"]))
        print("接口名称：{}".format(case["interface"]))
        print("接口名称：{}".format(case["title"]))
        print("预期结果：{}".format(expected))
        print("实际结果：{}".format(result))

        if case["interface"]=="uploadFileControl":
            fileId_uploadFileControl=jsonpath.jsonpath(result,"$..fileId")[0]
            conf.write_data("params","fileId_uploadFileControl",fileId_uploadFileControl)
        elif case["interface"] == "OpenReportFileList":
            fileIdOpenBid = jsonpath.jsonpath(result, "$..reportFileId")[0]
            fileIdWeiChuan= jsonpath.jsonpath(result, "$..reportFileId")[1]
            conf.write_data("params","fileIdOpenBid",fileIdOpenBid)
            conf.write_data("params","fileIdWeiChuan",fileIdWeiChuan)

        try:
            self.assertEqual(result["code"], expected["code"])
            self.assertEqual(result["msg"], expected["msg"])
        except AssertionError as e:
            self.excel.write_data(row=case["case_id"] + 1, column=9, value="不通过")
            my_log.info("用例：{}执行不通过".format(case["title"]))
            my_log.error(e)
            my_log.exception(e)
            raise e
        else:
            self.excel.write_data(row=case["case_id"] + 1, column=9, value="通过")
            my_log.info("用例：{}执行通过".format(case["title"]))


if __name__ == '__main__':
    unittest.main()
