from configparser import ConfigParser
from common.contents import CONF_DIR
import os


#非继承式封装
class MyConf:

    def __init__(self, filename, encoding="utf8"):
        """

        :param filename:配置文件
        :param encoding:文件编码方式
        """
        self.filename = filename;
        self.encoding = encoding;
        # 创建一个文件细解析器对象
        self.conf = ConfigParser()
        # 使用解析器对象，加载配置文件中的内容
        self.conf.read(filename, encoding)

    def get_str(self, section, option):
        # 读取数据
        """

        :param section:配置块
        :param option:配置项
        :return:对应配置项的数据
        """
        return self.conf.get(section, option)

    def get_int(self, section, option):
        # 读取数据
        """

        :param section:配置块
        :param option:配置项
        :return:对应配置项的数据
        """
        return self.conf.get(section, option)

    def get_float(self, section, option):
        # 读取数据
        """

        :param section:配置块
        :param option:配置项
        :return:对应配置项的数据
        """
        return self.conf.get(section, option)

    def get_boolean(self, section, option):
        # 读取数据
        """

        :param section:配置块
        :param option:配置项
        :return:对应配置项的数据
        """
        return self.conf.get(section, option)

    def write_data(self, section, option, value):
        """

        :param section: 配置块
        :param option: 配置项
        :param value:配置项对应的值
        :return:
        """
        # 写入内容
        self.conf.set(section, option, value)
        # 保存到文件
        self.conf.write(open(self.filename, "w", encoding=self.encoding))

#获取配置文件的绝对路径
#conf_path=r"D:\python24\py24_test_project\conf\conf.ini"
conf_path=os.path.join(CONF_DIR,"conf.ini")
conf=MyConf(conf_path)


