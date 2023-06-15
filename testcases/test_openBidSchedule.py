import unittest
from lib.ddt import ddt, data
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
class TestOpenBidSchedule(unittest.TestCase):
    excel_path = os.path.join(DATA_DIR, "cases.xlsx")
    excel = ReadExcel(excel_path, "openBidSchedule")
    cases = excel.read_data()
    http = HandRequests()
    db = HandleDB()

    @data(*cases)
    def test_openBidSchedule(self, case):

        headers = eval(conf.get_str("env", "headers"))
        if case["interface"] != "login":
            headers["Authorization"] = getattr(TestData, "cookie")

        method = case["method"]
        url = replace_data(conf.get_str("env", "url") + case["url"])

        if case["interface"] == "getJumpUrl" or \
                case["interface"] == "bidderList" or\
                case["interface"] == "tFileUpdateSignData" or\
                case["interface"] == "bUpdateSignDataNy" or\
                case["interface"] == "bUpdateSignDataNd"or\
                case["interface"] == "bUpdateSignDataYd" or\
                case["interface"] == "updateSignDataConfirm" or\
                case["interface"] == "signAllData" or\
                case["interface"] == "pubPage":

            data = replace_data(case["data"]).encode('UTF-8')
            response = self.http.send(headers=headers, method=method, url=url, data=data)
        elif case["method"] == "get":
            params = eval(replace_data(case["data"]))
            response = self.http.send(headers=headers, method=method, url=url, params=params)
        else:
            json = eval(replace_data(case["data"]))
            response = self.http.send(headers=headers, method=method, url=url, json=json)

        expected = eval(case["expected"])
        result = response.json()

        print("预期结果：{}".format(expected))
        print("实际结果：{}".format(result))

        if case["interface"] == "login":
            cookie = jsonpath.jsonpath(result, "$..cookieValue")[0]
            userCode=jsonpath.jsonpath(result,"$..userId")[0]
            userType=jsonpath.jsonpath(result,"$..userType")[0]
            setattr(TestData, "cookie", cookie)
            setattr(TestData,"userCode",userCode)
            setattr(TestData,"userType",userType)
        elif case["interface"]=="uploadFile":
            fileId=jsonpath.jsonpath(result,"$..fileld")[0]
            setattr(TestData,"fileId",fileId)
        elif case["interface"] == "createProjectByTenderFile":
            projectId = jsonpath.jsonpath(result, "$..projectId")[0]
            bidSectionId = jsonpath.jsonpath(result, "$..bidSectionId")[0]
            setattr(TestData, "projectId", projectId)
            setattr(TestData, "bidSectionId", bidSectionId)
            sql = case["check_sql"].format(getattr(TestData, "projectId"))
        elif case["interface"]=="projectlist":
            domainId=jsonpath.jsonpath(result,"$..domainId")[0]
            setattr(TestData,"domainId",domainId)
            print(domainId)
        elif case["interface"]=="getBidSectionBriefList":
            openBidId=jsonpath.jsonpath(result,"$..openBidId")[0]
            setattr(TestData,"openBidId",openBidId)
        elif case["interface"]=="bidderList":
            bidderId=jsonpath.jsonpath(result,"$..bidderId")[0]
            setattr(TestData,"bidderId",bidderId)
            bidderName=jsonpath.jsonpath(result,"$..bidderName")[0]
            setattr(TestData,"bidderName",bidderName)
            singedId=jsonpath.jsonpath(result,"$..singedId")[0]
            setattr(TestData,"singedId",singedId)

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
