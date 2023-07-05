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
from common.db import HandleDB


@ddt
class TestOpenPrepare(unittest.TestCase):
    excel_path = os.path.join(DATA_DIR, "cases.xlsx")
    excel = ReadExcel(excel_path, "openPrepare")
    cases = excel.read_data()
    http = HandRequests()
    db = HandleDB()

    @data(*cases)
    def test_openPrepare(self, case):

        global bidderIdList
        headers = eval(conf.get_str("env", "headers"))
        url = replace_data(conf.get_str("env", "url") + case["url"])


        if case["interface"] != "login":
            headers["Authorization"] = conf.get_str("params", "cookie")

        method = case["method"]
        expected = eval(case["expected"])

        if case["interface"] == "addBidder":
            # 遍历生成投标人
            for i in range(5):
                bidderName = str(i + 1)
                conf.write_data("params", "bidderName", bidderName)
                data = replace_data(case["data"]).encode('utf-8')
                print(data)
                response = self.http.send(headers=headers, method=method, url=url, params=data, data=data, json=data)
        # 投标文件递交状态修改：已递交
        elif case["interface"] == "tFileUpdateSignData":
            # 遍历键值对
            bidDic = eval(conf.get_str("params", "bidder_kv"))
            for k, v in bidDic.items():
                conf.write_data("params", "bidderId", str(k))
                conf.write_data("params", "bidderName", str(v))
                data = replace_data(case["data"]).encode('utf-8')
                response = self.http.send(headers=headers, method=method, url=url, params=data, data=data, json=data)
                # conf.delete_data("params", "bidderId")
                # conf.delete_data("params", "bidderName")
        # 确认投标单位
        elif case["interface"] == "updateSignDataConfirm":
            # 遍历键值对
            bidDic = eval(conf.get_str("params", "bidder_kv"))
            for k, v in bidDic.items():
                conf.write_data("params", "bidderId", str(k))
                conf.write_data("params", "bidderName", str(v))
                data = replace_data(case["data"]).encode('utf-8')
                response = self.http.send(headers=headers, method=method, url=url, params=data, data=data, json=data)
                # conf.delete_data("params","bidderId")
                # conf.delete_data("params", "bidderName")
        # 全部确认投标单位
        elif case["interface"] == "signAllData":
            # 遍历键值对
            bidderDic = eval(conf.get_str("params", "bidder_kv"))
            for k, v in bidderDic.items():
                conf.write_data("params", "bidderId", str(k))
                conf.write_data("params", "bidderName", str(v))
                data = replace_data(case["data"]).encode('utf-8')
                response = self.http.send(headers=headers, method=method, url=url, params=data, data=data,json=data)
                # conf.delete_data("params", "bidderId")
                # conf.delete_data("params", "bidderName")
        else:
            data = replace_data(case["data"]).encode('utf-8')
            response = self.http.send(headers=headers, method=method, url=url, params=data, data=data, json=data)

        result = response.json()
        print("接口序号：{}".format(case["case_id"]))
        print("接口名称：{}".format(case["interface"]))
        print("接口名称：{}".format(case["title"]))
        print("预期结果：{}".format(expected))
        print("实际结果：{}".format(result))

        if case["interface"] == "getBidSectionBriefList":
            openBidId = jsonpath.jsonpath(result, "$..openBidId")[0]
            conf.write_data("params", "openBidId", openBidId)
        elif case["interface"] == "bidderList":
            bidderIdList = jsonpath.jsonpath(result, "$..bidderId")
            bidderName = jsonpath.jsonpath(result, "$..bidderName")
            # 保存投标人id和name
            dic_bidder = {}
            for key, value in zip(bidderIdList, bidderName):
                dic_bidder[key] = value
            print(dic_bidder)
            conf.write_data("params", "bidder_kv", str(dic_bidder))

            singedId = jsonpath.jsonpath(result, "$..singedId")[0]
            conf.write_data("params", "singedId", singedId)

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
