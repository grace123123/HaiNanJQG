"""
============================
author:MuSen
time:2019/7/8
E-mail:3247119728@qq.com
============================
"""
import suds
from suds import client


class WebRequests(object):
    """发送webservice的请求"""

    def request(self, url, interface, data):

        # 发送请求获取地址接口
        self.web_s = client.Client(url=url)
        try:
            response = eval("self.web_s.service.{}({})".format(interface, data))
            # 此处发生异常说明，请求参数数据和服务器期望数据不匹配
        except suds.WebFault as e:
            # 返回错误的异常数据
            return dict(e.fault)
        else:
            # 返回正常的响应数据
            return dict(response)


if __name__ == '__main__':
    url = "http://120.24.235.105:9010/sms-service-war-1.0/ws/smsFacade.ws?wsdl"
    wb = WebRequests()
    res = wb.request(url=url, interface='sendMCode',
                     data={"client_ip": "120.132.11.14", "tmpl_id": "1", "mobile": "13342424534"})
    print(res)
