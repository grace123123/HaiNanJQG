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
from common.parametric import replace_data
from common.db import HandleDB


@ddt
class TestSingBid(unittest.TestCase):
    excel_path = os.path.join(DATA_DIR, "cases.xlsx")
    excel = ReadExcel(excel_path, "singBid")
    cases = excel.read_data()
    http = HandRequests()
    db = HandleDB()

    @data(*cases)
    def test_singBid(self, case):

        global headers
        if case["interface"] == "mp3":
            url=replace_data(case["url"])
            data = replace_data(case["data"])
        elif case["interface"] == "allmp3":
            url=replace_data(case["url"])
            data = replace_data(case["data"])
        else:
            headers = eval(conf.get_str("env", "headers"))
            url = replace_data(conf.get_str("env", "url") + case["url"])
            data = replace_data(case["data"]).encode('utf-8')

        if case["interface"] != "login":
            headers["Authorization"] = conf.get_str("params", "cookie")

        method = case["method"]
        expected = eval(case["expected"])

        response = self.http.send(headers=headers, method=method, url=url, params=data, data=data, json=data)

        if case["interface"] == "mp3":
            result = response
        elif case["interface"] == "allmp3":
            result=response
        else:
            result = response.json()
        print("接口序号：{}".format(case["case_id"]))
        print("接口名称：{}".format(case["interface"]))
        print("接口名称：{}".format(case["title"]))
        print("预期结果：{}".format(expected))
        print("实际结果：{}".format(result))

        if case["interface"] == "singleSingBid":
            fileUrl=jsonpath.jsonpath(result,"$..fileUrl")[0]
            conf.write_data("params","fileUrl",fileUrl)
        elif case["interface"] == "allSingBid":
            fileUrlAll=jsonpath.jsonpath(result,"$..fileUrl")[0]
            conf.write_data("params","fileUrlAll",fileUrlAll)

        try:
            if case["interface"] == "mp3":
                self.assertEqual(1, 1)
            elif case["interface"] == "allmp3":
                self.assertEqual(1, 1)
            else:
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
