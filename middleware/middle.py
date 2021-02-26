import os
import random
import re
from pymysql.cursors import DictCursor
from common.db_handler import DBHandler
from common.logger_handler import LoggerHandler
from common.yaml_handler import YamlHandler
from common.excel_handler import ExcelHandler
from config.path import  logs_path, data_path


class MidDBHandler(DBHandler):


    def __init__(self):
        yaml_config = YamlHandler('config.yaml').yaml_load()
        safe_config = YamlHandler('safe.yaml').yaml_load()
        super().__init__(host=safe_config['db']['host'],
                         port=safe_config['db']['port'],
                         user=safe_config['db']['user'],
                         password=safe_config['db']['password'],
                         # 不要写成utf-8
                         charset=safe_config['db']['charset'],
                         # 指定数据库
                         database=safe_config['db']['database'],
                         cursorclass=DictCursor)


class MidHandler():
    """任务：中间层。common和调用层，使用项目的配置数据，填充common模块"""
    # 设置属性
    new_phone = ''
    investor_user_id = ''
    investor_user_token = ''
    admin_user_id = ''
    admin_user_token = ''
    load_id = ''
    load_token = ''

    yaml_config = YamlHandler('config.yaml').yaml_load()
    safe_config = YamlHandler('safe.yaml').yaml_load()
    # logger获取
    log_file = os.path.join(logs_path, yaml_config['logger']['File'])
    logger = LoggerHandler(Logger_Name=yaml_config['logger']['Logger_Name'],
                           File=log_file,
                           Logger_Level=yaml_config['logger']['Logger_Level'],
                           Hand_Level=yaml_config['logger']['Hand_Level'],
                           File_Hand_Level=yaml_config['logger']['File_Hand_Level'])

    # 需要替换的数据
    investor_phone =safe_config['investor_user']['mobile_phone']
    investor_pwd = safe_config['investor_user']['pwd']
    admin_phone = safe_config['admin_user']['mobile_phone']
    admin_pwd = safe_config['admin_user']['pwd']
    loan_phone = safe_config['loan_user']['mobile_phone']
    loan_pwd = safe_config['loan_user']['pwd']

    @classmethod
    def replace_data(cls, string):
        '''替换表格数据函数'''
        pattern = '#(.*?)#'
        results = re.finditer(pattern=pattern, string=string)
        for result in results:
            old = result.group()
            key = result.group(1)
            new = str(getattr(cls, key, ''))
            string = string.replace(old, new)
        return string
    # excel对象
    excel_file = os.path.join(data_path, 'cases.xlsx')
    excel = ExcelHandler(excel_file)
    # excelwrite = ExcelHandler(excel_file).write('', '哈哈', row='', column='')
    # 数据库
    db_class = MidDBHandler

    @classmethod
    def random_number_1(cls):
        '''随机生成电话'''
        while True:
              mobile_number = '1' + random.choice(['3', '5'])
              for i in range(9):
                  mobile_number += str(random.randint(1, 9))
              sql = 'SELECT mobile_phone FROM member WHRER mobile_phone={};'.format(str(mobile_number))
              db = MidDBHandler()
              db_num = db.connect(sql, fetchone=True)
              if not db_num:
                # cls.new_phone = mobile_number
                return mobile_number


if __name__ == '__main__':
    sql = 'select leave_amount from member where id=2067;'
    data = MidHandler.db_class()
    info = data.connect(sql, fetchone=True)
    print(info)

    da=MidHandler.replace_data('{"mobile_phone":"#investor_phone#","pwd":"#investor_pwd#","mobile_phone":"#admin_phone#","mobile_phone":"#load_phone#","pwd":"#load_pwd#"}')
    print(da)
    new_phone = MidHandler.random_number_1()
    print(new_phone)