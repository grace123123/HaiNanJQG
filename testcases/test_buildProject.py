import unittest
from lib.ddt import ddt, data
from common.readexcel import ReadExcel
import os
from common.contents import DATA_DIR, RESOURCES_DIR
from common.request import HandRequests
from common.config import conf
from common.logger import my_log
import jsonpath
from common.parametric import TestData, replace_data
from common.db import HandleDB


@ddt
class TestBuildProject(unittest.TestCase):
    excel_path = os.path.join(DATA_DIR, "cases.xlsx")
    excel = ReadExcel(excel_path, "buildProject")
    cases = excel.read_data()
    http = HandRequests()
    db = HandleDB()

    @data(*cases)
    def test_buildProject(self, case):

        if case["interface"] == "uploadFile":
            headers = eval(conf.get_str("env", "headers1"))
            url = case["url"]

            # files={"file": ("", open(r"F:\pdf_file.pdf", "rb"), "pdf")}
            # file：固定值
            # ""：元组第一个值为文件名称，没有则取None
            # open(r"F:\pdf_file.pdf", "rb")：若第一个值非None，则取文件open打开的二进制流，否则直接写文件路径，如"F:\pdf_file.pdf"
            # pdf：文件类型，请求参数里一般会有，比如这里Content-Type: application/octet-stream

            file_path = os.path.join(RESOURCES_DIR, "zhao.GZBS")
            global file
            file= ("file",("zhao.GZBS",open(r"D:\workFile\jiqiguanshuili\zhao.GZBS", "rb"),"application/octet-stream"))
            #file= {'file',open(r'D:\workFile\jiqiguanshuili\zhao.GZBS', 'rb')}

            global data
            data = eval(replace_data(case["data"]))
            print(data)
        else:
            headers = eval(conf.get_str("env", "headers"))
            url = conf.get_str("env", "url") + case["url"]
            data = eval(case["data"])

        if case["interface"] != "login":
            headers["Authorization"] = getattr(TestData, "cookie")

        method = case["method"]
        expected = eval(case["expected"])

        if case["interface"] == "uploadFile":
            response = self.http.send(headers=headers, method=method, url=url,files=file,data=data)
        else:
            response = self.http.send(headers=headers, method=method, url=url, json=data)
        result = response.json()
        print(response.text)

        print("预期结果：{}".format(expected))
        print("实际结果：{}".format(result))

        if case["interface"] == "login":
            cookieValue = jsonpath.jsonpath(result, "$..cookieValue")[0]
            setattr(TestData, "cookie", cookieValue)
        elif case["interface"]=="getUploadUrl":
            logicPath = jsonpath.jsonpath(result, "$..logicPath")[0]
            setattr(TestData, "logicPath", logicPath)
            print("logicPath:"+logicPath)
        elif case["interface"]=="uploadFile":
            fileId=jsonpath.jsonpath(result,"$..fileld")[0]
            setattr(TestData,"fileId",fileId)
        if case["interface"] == "createProjectByTenderFile":
            projectId = jsonpath.jsonpath(result, "$..projectId")[0]
            setattr(TestData, "projectId", projectId)
            sql = case["check_sql"].format(getattr(TestData, "projectId"))
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
