import unittest
from lib.ddt import ddt, data
from common.readexcel import ReadExcel
import os
from common.contents import DATA_DIR
from common.request import HandRequests
from common.config import conf
from common.logger import my_log
import jsonpath
from common.parametric import TestData,replace_data


@ddt
class TestSearchProjectList(unittest.TestCase):

    excel_path=os.path.join(DATA_DIR,"cases.xlsx")
    excel=ReadExcel(excel_path,"searchProjectList")
    cases=excel.read_data()
    http=HandRequests()

    @data(*cases)
    def test_searchProjectList(self,case):

        headers=eval(conf.get_str("env","headers"))
        if case["interface"]!="login":
            headers["Authorization"]=getattr(TestData,"cookie")
        method=case["method"]
        url=conf.get_str("env","url")+case["url"]
        data=eval(case["data"])
        expected=eval(case["expected"])

        response=self.http.send(headers=headers,method=method,url=url,json=data)
        result=response.json()

        print("预期结果：{}".format(expected))
        print("实际结果：{}".format(result))

        if case["interface"]=="login":
            cookieValue = jsonpath.jsonpath(result, "$..cookieValue")[0]
            setattr(TestData,"cookie",cookieValue)

        try:
            self.assertEqual(result["code"],expected["code"])
            self.assertEqual(result["msg"],expected["msg"])
        except AssertionError as e:
            self.excel.write_data(row=case["case_id"]+1,column=8,value="不通过")
            my_log.info("用例：{}执行未通过".format(case["title"]))
            my_log.error(e)
            my_log.exception(e)
            raise e
        else:
            self.excel.write_data(row=case["case_id"]+1,column=8,value="通过")
            my_log.info("用例：{}执行通过".format(case["title"]))


if __name__ == '__main__':
    unittest.main()