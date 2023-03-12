import pymysql
from common.config import conf

class HandleDB:

    def __init__(self):
        # 连接数据库
        self.con = pymysql.connect(
            # host=conf.get_str("mysql","host"),
            # port=conf.get_int("mysql", "port"),
            # user=conf.get_str("mysql","user"),
            # password=conf.get_str("mysql","password"),
            host='10.0.106.3',
            port=3306,
            user='root',
            password='Root@123',
            database='gbes',
            charset='utf8')

        self.cur = self.con.cursor()

    def get_one(self, sql):
        # 使用pymysql操作数据库默认会开启事务(原子性，一致性，隔离性，持久性)，连接数据库，创建游标表示开启了一个事务
        # 查询之前先提交，是因为可能在开启事务之后，开始查询之前有新的操作，为了查询数据保持最新状态所以要提交
        #self.con.commit()
        self.cur.execute(sql)
        return self.cur.fetchone()

    def get_all(self, sql):
        self.con.commit()
        self.cur.execute(sql)
        return self.cur.fetchall()

    def count(self, sql):
        self.con.commit()
        res = self.cur.execute(sql)
        return res

    def delete(self,sql):
        self.cur.execute(sql)
        self.con.commit()

    def close(self):
        self.con.commit()
        # 关闭游标对象
        self.cur.close()
        # 断开连接
        self.con.close()
