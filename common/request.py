"""
封装的目的：


封装的需求：
发送post请求，发送get请求，发送patch请求
如何做到不同请求方式的接口去发送不同的请求
加判断
"""
import requests

class HandRequests():

    #这里url,params,json,headers都给了一个默认值，如果以后要传新的参数会覆盖掉默认值，不传的话也没影响，因为有默认值
    def send(self,method,url=None,params=None,data=None,json=None,files=None,headers=None):       #files=None,
        #将请求的方法转换为小写
        method=method.lower()
        if method=="post":
            return requests.post(url=url,json=json,data=data,files=files,headers=headers)
        elif method=="patch":
            return requests.patch(url=url,json=json,data=data,headers=headers)
        elif method=="get":
            return requests.get(url=url,params=params,headers=headers)

class HandleSessionRequest:

    #处理使用session鉴权的接口使用这个类来发送请求
    def __init__(self):
        self.se=requests.session()

    def send(self, method, url=None, params=None, data=None, json=None, files=None,headers=None):
        # 将请求的方法转换为小写
        method = method.lower()
        if method == "post":
            return self.se.post(url=url, json=json, data=data,files=files, headers=headers)
        elif method == "patch":
            return self.se.patch(url=url, json=json, data=data, headers=headers)
        elif method == "get":
            return self.se.get(url=url, params=params, headers=headers)


if __name__=='__main__':
    login_url = "http://api.lemonban.com/futureloan/member/login"

    header = {
        "X-Lemonban-Media-Type": "lemonban.v2",
        "Content-Type": "application/json"
    }

    data = {
        "mobile_phone": "15567899803",
        "pwd": "123456qwe",
    }

    http=HandRequests()
    res=http.send(url=login_url,method="post",json=data,headers=header)
    print(res.json())


