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
class TestDecrypt(unittest.TestCase):
    excel_path = os.path.join(DATA_DIR, "cases.xlsx")
    excel = ReadExcel(excel_path, "decrypt")
    cases = excel.read_data()
    http = HandRequests()
    db = HandleDB()

    @data(*cases)
    def test_decrypt(self, case):

        # 上传投标文件
        global headers, headers_uploadFilePiece, url_uploadFilePiece, files_uploadFilePiece, data_uploadFilePiece, url, data, f, fildId_filePathDic, fileInformationDic
        if case["interface"] == "uploadFilePiece":
            headers_uploadFilePiece = eval(conf.get_str("env", "headers1"))
            url_uploadFilePiece = case["url"]
        else:
            headers = eval(conf.get_str("env", "headers"))
            url = replace_data(conf.get_str("env", "url") + case["url"])
            data = replace_data(case["data"]).encode('utf-8')

        if case["interface"] != "login":
            headers["Authorization"] = conf.get_str("params", "cookie")

        method = case["method"]
        expected = eval(case["expected"])

        # 接口3：上传投标文件
        if case["interface"] == "uploadFilePiece":
            # 遍历键值对，获取bidderId，bidderName
            bidDic = eval(conf.get_str("params", "bidder_kv"))
            for k, v in bidDic.items():
                conf.write_data("params", "bidderId", str(k))
                conf.write_data("params", "bidderName", str(v))
                data_uploadFilePiece = eval(replace_data(case["data"]))
                # 文件处理
                fileName = "房建施工{}.GTBS".format(v)
                filePath = "D:\\HaiNanJQG\\resources\\{}".format(fileName)
                f = open(filePath, "rb")
                files_uploadFilePiece = {"file": (fileName, f, "application/octet-stream")}
                response = self.http.send(headers=headers_uploadFilePiece, method=method, url=url_uploadFilePiece,
                                          files=files_uploadFilePiece, data=data_uploadFilePiece)
                result = response.json()
                # 提取fileId和filePath
                fileId = jsonpath.jsonpath(result, "$..fileId")[0]
                filePath = jsonpath.jsonpath(result, "$..filePath")[0]
                # 循环保存投标人fileId和filePath
                fildId_filePathDic = {}
                fildId_filePathDic[fileId] = filePath
                conf.write_data("params", "fileId_filePath_kv", str(fildId_filePathDic))
                try:
                    self.assertEqual(result["fileSize"], expected["fileSize"])
                except AssertionError as e:
                    self.excel.write_data(row=case["case_id"] + 1, column=9, value="不通过")
                    my_log.info("用例：{}执行不通过".format(case["title"]))
                    my_log.error(e)
                    my_log.exception(e)
                    raise e
                else:
                    self.excel.write_data(row=case["case_id"] + 1, column=9, value="通过")
                    my_log.info("用例：{}执行通过".format(case["title"]))

        # 接口4：获取投标文件信息
        if case["interface"] == "getFileInfo":
            # 遍历获取fileId
            for i in fildId_filePathDic:

                conf.write_data("params", "fileId", i)
                url = replace_data(conf.get_str("env", "url") + case["url"])

                response = self.http.send(headers=headers, method=method, url=url, params=data, data=data,json=data)
                result=response.json()
                #提取fileName，fileMd5，fileExt，diskFileName，parentFileId，createTime，diskFilePath，fileSize，operTime
                fileId = jsonpath.jsonpath(result, "$..fileId")[0]
                json=expected["obj"]
                fileInformationDic={}
                fileInformationDic[fileId]=json
                conf.write_data("params","fileInformatiionDic",fileInformationDic)

        # 接口5：获取解密页投标单位数据
        if case["interface"] == "decryptListPage":
            response = self.http.send(headers=headers, method=method, url=url, params=data, data=data, json=data)
            result=response.json()
            bidderId = jsonpath.jsonpath(result, "$..bidderId")
            id = jsonpath.jsonpath(result, "$..id")
            idDic={}
            for key, value in zip(bidderId, id):
                idDic[key] = value
            conf.write_data("params", "idDic_kv", str(idDic))
            # digitalEnvelope_decryptListPage = jsonpath.jsonpath(result, "$..digitalEnvelope")[0]
            # conf.write_data("params", "digitalEnvelope_decryptListPage", digitalEnvelope_decryptListPage)
        # 接口6：获取解密页投标单位数据
        if case["interface"] == "getCountStatistics":
            response = self.http.send(headers=headers, method=method, url=url, params=data, data=data, json=data)

        # 接口7：投标文件解析
        if case["interface"] == "praseFile":
            # 遍历获取fileId
            for i in fileInformationDic:
                conf.write_data("params", "fileId", i)
                obj=conf.get_str("params","fileId")
                #参数化
                fileName = jsonpath.jsonpath(obj, "$..fileName")[0]
                fileMd5 = jsonpath.jsonpath(obj, "$..fileMd5")[0]
                fileExt = jsonpath.jsonpath(obj, "$..fileExt")[0]
                diskFileName = jsonpath.jsonpath(obj, "$..diskFileName")[0]
                parentFileId = jsonpath.jsonpath(obj, "$..parentFileId")[0]
                createTime = jsonpath.jsonpath(obj, "$..createTime")[0]
                diskFilePath = jsonpath.jsonpath(obj, "$..diskFilePath")[0]
                fileSize = str(jsonpath.jsonpath(obj, "$..fileSize")[0])
                operTime = jsonpath.jsonpath(obj, "$..operTime")[0]
                conf.write_data("params", "fileName", fileName)
                conf.write_data("params", "fileMd5", fileMd5)
                conf.write_data("params", "fileExt", fileExt)
                conf.write_data("params", "diskFileName", diskFileName)
                conf.write_data("params", "parentFileId", parentFileId)
                conf.write_data("params", "createTime", createTime)
                conf.write_data("params", "diskFilePath", diskFilePath)
                conf.write_data("params", "fileSize", fileSize)
                conf.write_data("params", "operTime", operTime)
                data = replace_data(case["data"]).encode('utf-8')
            response = self.http.send(headers=headers, method=method, url=url, params=data, data=data, json=data)

        #接口8：通过id解析
        if case["interface"] == "decryptById":
            #遍历获取id
            for j in fildId_filePathDic.values():
                conf.write_data("params", "id", j)
                url = replace_data(conf.get_str("env", "url") + case["url"])
                response = self.http.send(headers=headers, method=method, url=url, params=data, data=data, json=data)

        #接口9：获取数字信封
        if case["interface"] == "getDigitalEnvelope":
            response = self.http.send(headers=headers, method=method, url=url, params=data, data=data, json=data)
            result=response.json()
            degitalEnvelope_getDigitalEnvelope = jsonpath.jsonpath(result, "$..degitalEnvelope")[0]
            conf.write_data("params", "degitalEnvelope_getDigitalEnvelope",degitalEnvelope_getDigitalEnvelope)

        # 接口10：更新数字信封
        if case["interface"] == "updateDigitalEnvelope":
            response = self.http.send(headers=headers, method=method, url=url, params=data, data=data, json=data)
        if case["interface"] == "getDecryptSpeed":
            for i in range(1000):
                response = self.http.send(headers=headers, method=method, url=url, params=data, data=data,
                                          json=data)
            result = response.json()

        else:
            response = self.http.send(headers=headers, method=method, url=url, params=data, data=data, json=data)


        result = response.json()
        print("接口序号：{}".format(case["case_id"]))
        print("接口名称：{}".format(case["interface"]))
        print("接口名称：{}".format(case["title"]))
        print("预期结果：{}".format(expected))
        print("实际结果：{}".format(result))

        # try:
        #     if case["interface"] == "uploadFilePiece":
        #         self.assertEqual(result["fileSize"], expected["fileSize"])
        #     elif case["interface"] == "mp3":
        #         self.assertEqual(1, 1)
        #     elif case["interface"] == "allmp3":
        #         self.assertEqual(1, 1)
        #     else:
        #         self.assertEqual(result["code"], expected["code"])
        #         self.assertEqual(result["msg"], expected["msg"])
        # except AssertionError as e:
        #     self.excel.write_data(row=case["case_id"] + 1, column=9, value="不通过")
        #     my_log.info("用例：{}执行不通过".format(case["title"]))
        #     my_log.error(e)
        #     my_log.exception(e)
        #     raise e
        # else:
        #     self.excel.write_data(row=case["case_id"] + 1, column=9, value="通过")
        #     my_log.info("用例：{}执行通过".format(case["title"]))

if __name__ == '__main__':
    unittest.main()
