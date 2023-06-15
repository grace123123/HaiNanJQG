import random


def random_phone():
    phone = "133"
    for i in range(8):
        phone += str(random.randint(0, 9))
    return phone


# def random_phone1(cls):
#     """生成随机的手机号码"""
#     while True:
#         phone = "133"
#         for i in range(8):
#             phone += str(random.randint(0, 9))
#         # 应该在去数据库查询一下，看数据库中该手机号码是否已被注册
#         sql = "SELECT * FROM futureloan.member WHERE mobile_phone={}".format(phone)
#         num = cls.db.count(sql)
#         if num == 0:
#             return phone
