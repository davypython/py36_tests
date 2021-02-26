
import openpyxl
from openpyxl.worksheet.worksheet import Worksheet


class ExcelHandler:
    def __init__(self,xpath):
        '''初始化表格路径对象'''
        self.xpath = xpath
    def read(self,sheetname):
        '''读取表格数据，生成列表嵌套字典格式输出'''
        workbook = openpyxl.open(self.xpath)
        worksheet : Worksheet = workbook[sheetname]
        ws_v=list(worksheet.values)
        data=[]
        data_title = ws_v[0]
        data_list = ws_v[1:]
        for i in data_list:
            data_dict=dict(zip(data_title,i))
            data.append(data_dict)

        return data
    def write(self,sheetname,data,row,column):
        '''写入表格数据'''
        workbook = openpyxl.open(self.xpath)
        worksheet: Worksheet = workbook[sheetname]
        worksheet.cell(row=row,column=column).value = data
        workbook.save(self.xpath)
        workbook.close()
