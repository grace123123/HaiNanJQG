import unittest
from library.ddt import ddt, data
from common.readexcel import ReadExcel
import os
from common.contents import DATA_DIR
from common.request import HandRequests
from common.config import conf
from common.logger import my_log
import jsonpath
from common.parametric import TestData, replace_data
from common.contents import CONF_DIR
from common.config import MyConf

@ddt
class TestLogin(unittest.TestCase):
    excel_path = os.path.join(DATA_DIR, "cases.xlsx")
    excel = ReadExcel(excel_path, "login")
    cases = excel.read_data()
    http = HandRequests()

    confDir = os.path.join(CONF_DIR, "conf.ini")
    conf = MyConf(confDir)


    @data(*cases)
    def test_login(self, case):
        headers= eval(conf.get_str("env", "headers"))
        method = case["method"]
        url = replace_data(conf.get_str("env", "url") + case["url"])
        data = eval(replace_data(case["data"]))
        expected = eval(case["expected"])

        if case["interface"] != "login":
            headers["Authorization"] = conf.get_str("params","cookie")

        response = self.http.send(headers=headers, method=method, url=url, json=data)
        result = response.json()

        print("接口序号：{}".format(case["case_id"]))
        print("接口名称：{}".format(case["interface"]))
        print("接口名称：{}".format(case["title"]))
        print("预期结果：{}".format(expected))
        print("实际结果：{}".format(result))

        if case["interface"] == "login":
            cookie = jsonpath.jsonpath(result, "$..cookieValue")[0]
            userCode = jsonpath.jsonpath(result, "$..userId")[0]
            userType = jsonpath.jsonpath(result, "$..userType")[0]
            conf.write_data("params","cookie", cookie)
            conf.write_data("params", "userCode", userCode)
            conf.write_data("params", "userType", userType)

        try:
            self.assertEqual(result["code"], expected["code"])
            self.assertEqual(result["msg"], expected["msg"])
        except AssertionError as e:
            self.excel.write_data(row=case["case_id"] + 1, column=9, value="未通过")
            my_log.info("用例：{}执行未通过".format(case["title"]))
            my_log.error(e)
            my_log.exception(e)
            raise e
        else:
            self.excel.write_data(row=case["case_id"] + 1, column=9, value="通过")
            my_log.info("用例：{}执行通过".format(case["title"]))


if __name__ == '__main__':
    unittest.main()
