import openpyxl


# 用来保存用例数据
class CaseData:
    pass


class ReadExcel():

    def __init__(self, filename, sheetname):
        self.filename = filename
        self.sheetname = sheetname

    def open(self):
        """打开工作簿，选中表单"""
        self.wb = openpyxl.load_workbook(self.filename)
        self.sh = self.wb[self.sheetname]

    def close(self):
        self.wb.close()

    def read_data(self):
        self.open()
        # 按行获取所有的数据
        rows = list(self.sh.rows)
        # 获取表头
        title = []
        for i in rows[0]:
            title.append(i.value)

        # 用来存放所有的用例数据
        cases = []
        # 遍历除了表头剩余的行
        for row in rows[1:]:
            # print(row)
            # 创建一个空列表，存储该行的数据
            data = []
            # 再次遍历该行的每一个格子
            for r in row:
                # 将格子中的数据添加到data中
                data.append(r.value)

            case = dict(zip(title, data))
            # print(case)
            cases.append(case)
        self.close()
        return cases   #列表嵌套字典

    def read_data_obj(self):

        self.open()
        # 按行获取所有的数据
        rows = list(self.sh.rows)
        # 获取表头
        title = []
        for i in rows[0]:
            title.append(i.value)

        # 用来存放所有的用例数据
        cases = []
        # 遍历除了表头剩余的行
        for row in rows[1:]:
            # print(row)
            # 创建一个空列表，存储该行的数据
            data = []
            # 再次遍历该行的每一个格子
            for r in row:
                # 将格子中的数据添加到data中
                data.append(r.value)
            # 将表头和数据打包转换为列表
            case = list(zip(title, data))
            # 创建一个对象用来保存该行用例数据
            case_obj = CaseData()
            # 遍历列表中该行用例数据，使用setattr设置为对象的属性和属性值
            for k, v in case:
                # print(k,v)
                setattr(case_obj, k, v)
            # print(case_obj, case_obj.__dict__)
            # 将对象添加到cases这个列表中
            cases.append(case_obj)
            # 返回cases(包含所有用例数据对象的列表)
        self.close()
        return cases   #列表嵌套对象

    def write_data(self, row, column,value):  # row,column,value不同于filename，sheetname要放在init方法里初始化，是因为filename,sheetname是作为属性被用到,而它们是作为值被用到。
        self.open()  # 一个是给对象传值，一个是给方法传值"
        self.sh.cell(row=row, column=column, value=value)
        self.wb.save(self.filename)
        self.close()


if __name__ == '__main__':  # 当你要导入某个模块，但又不想改模块的部分代码被直接执行，那就可以这一部分代码放在“if __name__=='__main__':”内部
    excel = ReadExcel("cases.xlsx", "login")
    data = excel.read_data()
    print(data)
