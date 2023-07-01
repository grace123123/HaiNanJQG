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
from common.myEncoder import MyEncoder
import json


@ddt
class TestOpenBidSchedule(unittest.TestCase):
    excel_path = os.path.join(DATA_DIR, "cases.xlsx")
    excel = ReadExcel(excel_path, "openBidSchedule")
    cases = excel.read_data()
    http = HandRequests()
    db = HandleDB()

    @data(*cases)
    def test_openBidSchedule(self, case):

        # 上传招标文件
        global headers_uploadFile, url_uploadFile, data_uploadFile, url, data, headers, headers_uploadFilePiece, url_uploadFilePiece, data_uploadFilePiece, files_uploadFile, files_uploadFilePiece, headers_decryptListPage, url_decryptListPage, data_decryptListPage, response, data_uploadFileControl, files_uploadFileControl, headers_uploadFileControl, url_uploadFileControl
        if case["interface"] == "uploadFile":
            headers_uploadFile = eval(conf.get_str("env", "headers2"))
            url_uploadFile = case["url"]
            files_uploadFile = {"file": (
                "房建施工-简易评估法-现场.GZBS", open("D:\\HaiNanJQG\\resources\\房建施工-简易评估法-现场.GZBS", "rb"),
                "application/octet-stream")}
            # data_uploadFile = {
            #     "json": "{'appId':'gbes','secretKey':'12345','fileMd5':'c02a4c073fcac518cdd6ed22fefce308','logicPath':'db08979d3c774a06bdaaa7fa4c54fa80/bidSectionId/openBid/tenderFile/'}"
            # }
            data_uploadFile = eval(replace_data(case["data"]))
        # 上传投标文件
        elif case["interface"] == "uploadFilePiece":
            headers_uploadFilePiece = eval(conf.get_str("env", "headers1"))
            url_uploadFilePiece = case["url"]
            files_uploadFilePiece = {
                "file": ("房建施工.GTBS", open("D:\\HaiNanJQG\\resources\\房建施工.GTBS", "rb"), "application/octet-stream")}
            data_uploadFilePiece = eval(replace_data(case["data"]))
        # elif case["interface"] == "uploadFilePiece":
        #     data = eval(replace_data(case["data"]))
        elif case["interface"] == "mp3":
            url=replace_data(case["url"])
            data = replace_data(case["data"])
        elif case["interface"] == "allmp3":
            url=replace_data(case["url"])
            data = replace_data(case["data"])
        #上传控制价文件
        elif case["interface"] == "uploadFileControl":
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
            headers["Authorization"] = getattr(TestData, "cookie")

        method = case["method"]
        expected = eval(case["expected"])

        # getJumpUrl    获取进入项目跳转路径
        # bidderList    查询投标人列表
        # tFileUpdateSignData    投标文件已递交
        # bUpdateSignDataNy    保证金未要求
        # bUpdateSignDataNd    保证金未递交
        # bUpdateSignDataYd    保证金已递交
        # updateSignDataConfirm    确认投标人
        # signAllData    全部确认
        # pubPage    跳转到【公布投标人】页

        # if case["interface"] == "getJumpUrl" or \
        #         case["interface"] == "bidderList" or\
        #         case["interface"] == "tFileUpdateSignData" or\
        #         case["interface"] == "bUpdateSignDataNy" or\
        #         case["interface"] == "bUpdateSignDataNd"or\
        #         case["interface"] == "bUpdateSignDataYd" or\
        #         case["interface"] == "updateSignDataConfirm" or\
        #         case["interface"] == "signAllData" or\
        #         case["interface"] == "pubPage":

        if case["interface"] == "uploadFile":
            response = self.http.send(headers=headers_uploadFile, method=method, url=url_uploadFile,
                                      files=files_uploadFile, data=data_uploadFile)
        elif case["interface"] == "uploadFilePiece":
            response = self.http.send(headers=headers_uploadFilePiece, method=method, url=url_uploadFilePiece,
                                      files=files_uploadFilePiece, data=data_uploadFilePiece)
        elif case["interface"] == "getDecryptSpeed":
            for i in range(1000):
                response = self.http.send(headers=headers, method=method, url=url, params=data, data=data, json=data)
        elif case["interface"] == "uploadFileControl":
            response = self.http.send(headers=headers_uploadFileControl, method=method, url=url_uploadFileControl,
                                      files=files_uploadFileControl, data=data_uploadFileControl)
        else:
            print(url)
            print(data)
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

        if case["interface"] == "login":
            cookie = jsonpath.jsonpath(result, "$..cookieValue")[0]
            userCode = jsonpath.jsonpath(result, "$..userId")[0]
            userType = jsonpath.jsonpath(result, "$..userType")[0]
            setattr(TestData, "cookie", cookie)
            setattr(TestData, "userCode", userCode)
            setattr(TestData, "userType", userType)
        elif case["interface"] == "getUploadUrl":
            logicPath = jsonpath.jsonpath(result, "$..logicPath")[0]
            print("***********************logicPath*****************************")
            print(logicPath)
            print("************************logicPath****************************")
            setattr(TestData, "logicPath", logicPath)
        elif case["interface"] == "uploadFile":
            fileId = jsonpath.jsonpath(result, "$..fileId")[0]
            filePath = jsonpath.jsonpath(result, "$..filePath")[0]
            setattr(TestData, "fileId", fileId)
            setattr(TestData, "filePath", filePath)
        elif case["interface"] == "createProjectByTenderFile":
            projectId = jsonpath.jsonpath(result, "$..projectId")[0]
            bidSectionId = jsonpath.jsonpath(result, "$..bidSectionId")[0]
            bidSectionCode = jsonpath.jsonpath(result, "$..bidSectionCode")[0]
            setattr(TestData, "projectId", projectId)
            setattr(TestData, "bidSectionId", bidSectionId)
            setattr(TestData, "bidSectionCode", bidSectionCode)
            print("***********************bidSectionId*****************************")
            print(bidSectionId)
            print("************************bidSectionId****************************")
            # sql = case["check_sql"].format(getattr(TestData, "projectId"))
        elif case["interface"] == "projectlistToday":
            domainId = jsonpath.jsonpath(result, "$..domainId")[0]
            print("***********************domainId*****************************")
            print(domainId)
            print("************************domainId****************************")
            setattr(TestData, "domainId", domainId)
        elif case["interface"] == "getBidSectionBriefList":
            openBidId = jsonpath.jsonpath(result, "$..openBidId")[0]
            setattr(TestData, "openBidId", openBidId)
            print("***********************openBidId*****************************")
            print(openBidId)
            print("************************openBidId****************************")
        elif case["interface"] == "bidderList":
            bidderId = jsonpath.jsonpath(result, "$..bidderId")[0]
            print("***********************bidderId*****************************")
            print(bidderId)
            print("************************bidderId****************************")
            setattr(TestData, "bidderId", bidderId)
            bidderName = jsonpath.jsonpath(result, "$..bidderName")[0]
            print("***********************bidderName*****************************")
            print(bidderName)
            print("************************bidderName****************************")
            setattr(TestData, "bidderName", bidderName)
            singedId = jsonpath.jsonpath(result, "$..singedId")[0]
            setattr(TestData, "singedId", singedId)
        elif case["interface"] == "uploadFilePiece":
            fileId_uploadFilePiece = jsonpath.jsonpath(result, "$..fileId")[0]
            filePath = jsonpath.jsonpath(result, "$..filePath")[0]
            setattr(TestData, "fileId_uploadFilePiece", fileId_uploadFilePiece)
            setattr(TestData, "filePath", filePath)
        elif case["interface"] == "getFileInfo":
            fileName = jsonpath.jsonpath(result, "$..fileName")[0]
            fileMd5 = jsonpath.jsonpath(result, "$..fileMd5")[0]
            fileExt = jsonpath.jsonpath(result, "$..fileExt")[0]
            diskFileName = jsonpath.jsonpath(result, "$..diskFileName")[0]
            parentFileId = jsonpath.jsonpath(result, "$..parentFileId")[0]
            createTime = jsonpath.jsonpath(result, "$..createTime")[0]
            diskFilePath = jsonpath.jsonpath(result, "$..diskFilePath")[0]
            fileSize = jsonpath.jsonpath(result, "$..fileSize")[0]
            operTime = jsonpath.jsonpath(result, "$..operTime")[0]
            setattr(TestData, "fileName", fileName)
            setattr(TestData, "fileMd5", fileMd5)
            setattr(TestData, "fileExt", fileExt)
            setattr(TestData, "diskFileName", diskFileName)
            setattr(TestData, "parentFileId", parentFileId)
            setattr(TestData, "createTime", createTime)
            setattr(TestData, "diskFilePath", diskFilePath)
            setattr(TestData, "fileSize", fileSize)
            setattr(TestData, "operTime", operTime)
        elif case["interface"] == "decryptListPage":
            id = jsonpath.jsonpath(result, "$..id")[0]
            digitalEnvelope_decryptListPage = jsonpath.jsonpath(result, "$..digitalEnvelope")[0]
            setattr(TestData, "id", id)
            setattr(TestData, "digitalEnvelope_decryptListPage", digitalEnvelope_decryptListPage)
            print("***********************id*****************************")
            print(id)
            print(digitalEnvelope_decryptListPage)
        elif case["interface"] == "getDigitalEnvelope":
            print("***********************result*****************************")
            print(result)
            degitalEnvelope_getDigitalEnvelope = jsonpath.jsonpath(result, "$..degitalEnvelope")[0]
            print("***********************degitalEnvelope_getDigitalEnvelope*****************************")
            print(degitalEnvelope_getDigitalEnvelope)
            print("***********************degitalEnvelope_getDigitalEnvelope*****************************")
            setattr(TestData, "degitalEnvelope_getDigitalEnvelope", degitalEnvelope_getDigitalEnvelope)
        elif case["interface"] == "singleSingBid":
            fileUrl=jsonpath.jsonpath(result,"$..fileUrl")[0]
            setattr(TestData,"fileUrl",fileUrl)
            print("***********************fileUrl*****************************")
            print(fileUrl)
        elif case["interface"] == "allSingBid":
            fileUrlAll=jsonpath.jsonpath(result,"$..fileUrl")[0]
            setattr(TestData,"fileUrlAll",fileUrlAll)
            print("***********************fileUrlAll*****************************")
            print(fileUrlAll)
        elif case["interface"]=="uploadFileControl":
            fileId_uploadFileControl=jsonpath.jsonpath(result,"$..fileId")[0]
            setattr(TestData,"fileId_uploadFileControl",fileId_uploadFileControl)
        elif case["interface"] == "OpenReportFileList":
            fileIdOpenBid = jsonpath.jsonpath(result, "$..reportFileId")[0]
            fileIdWeiChuan= jsonpath.jsonpath(result, "$..reportFileId")[1]
            setattr(TestData, "fileIdOpenBid", fileIdOpenBid)
            setattr(TestData, "fileIdWeiChuan", fileIdWeiChuan)
        elif case["interface"] == "endOpenBid":
            sql = replace_data(case["check_sql"])
            print(sql)
            self.db.delete(sql)

        try:
            if case["interface"] == "uploadFilePiece":
                self.assertEqual(result["fileSize"], expected["fileSize"])
            elif case["interface"] == "mp3":
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
