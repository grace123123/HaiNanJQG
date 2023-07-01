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
from urllib3 import encode_multipart_formdata
import request

@ddt
class TestBuildProject(unittest.TestCase):
    excel_path = os.path.join(DATA_DIR, "cases.xlsx")
    excel = ReadExcel(excel_path, "buildProject")
    cases = excel.read_data()
    http = HandRequests()
    db = HandleDB()

    @data(*cases)
    def test_buildProject(self, case):

        global files
        if case["interface"] == "uploadFile":
            headers = eval(conf.get_str("env", "headers2"))
            url= case["url"]

            files={"file":("水利监理-一次平均.GZBS",open("D:\\HaiNanJQG\\resources\\水利监理-一次平均.GZBS", "rb"),"application/octet-stream")}
            data={
                # "name": "file",
                # "filename": "水利监理-一次平均.GZBS",
                # "Content-Type": "application/octet-stream",
                # "Content-Disposition": "form-data",
                "json":"{'appId':'gbes','secretKey':'12345','fileMd5':'c02a4c073fcac518cdd6ed22fefce308','logicPath':'db08979d3c774a06bdaaa7fa4c54fa80/bidSectionId/openBid/tenderFile/'}"
                 }

        else:
            headers = eval(conf.get_str("env", "headers"))
            url= conf.get_str("env", "url") + case["url"]
            data= eval(case["data"])

        if case["interface"] != "login":
            headers["Authorization"] = getattr(TestData, "cookie")

        method = case["method"]
        expected = eval(case["expected"])

        if case["interface"] == "uploadFile":
            response = self.http.send(headers=headers,method=method, url=url,files=files,data=data)
        else:
            response = self.http.send(headers=headers, method=method, url=url, json=data)
        result = response.json()

        print("预期结果：{}".format(expected))
        print("实际结果：{}".format(result))

        if case["interface"] == "login":
            cookieValue = jsonpath.jsonpath(result, "$..cookieValue")[0]
            setattr(TestData, "cookie", cookieValue)
        if case["interface"]=="getUploadUrl":
            logicPath = jsonpath.jsonpath(result, "$..logicPath")[0]
            setattr(TestData, "logicPath", logicPath)
        if case["interface"]=="uploadFile":
            fileId=jsonpath.jsonpath(result,"$..fileld")
            filePath=jsonpath.jsonpath(result,"$..filePath")
            setattr(TestData,"fileId",fileId)
            setattr(TestData,"filePath",filePath)
        elif case["interface"] == "createProjectByTenderFile":
            projectId = jsonpath.jsonpath(result, "$..projectId")[0]
            setattr(TestData, "projectId", projectId)
            sql=replace_data(case["check_sql"])
            print(sql)
            self.db.delete(sql)

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
