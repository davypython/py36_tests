
import pymysql
from pymysql.cursors import DictCursor



"""
数据库操作
1.连接数据库
2.获取游标（标记）
3.执行（发起请求）
4.获取结果
5.关闭数据库和游标
"""

class DBHandler:
    '''数据库封装'''

    def __init__(self,
                 host='',
                 port=3306,
                 user='',
                 password='',
                 charset='utf8',
                 database='',
                 cursorclass=DictCursor):
        '''初始化连接数据库，并且读取yaml的数据库配置'''
        self.conn= pymysql.connect(host=host,
                       port=port,
                       user=user,
                       password=password,
                       charset=charset, # 字符格式 不能是utf-8
                       database=database,
                        cursorclass=cursorclass)
    def connect(self,sql,fetchone=True):
        '''连接数据库，获取数据库数据'''
        # 获取数据库类游标对象
        cursor=self.conn.cursor()
        self.conn.commit()
        try:
            cursor.execute(sql)
            if fetchone == True:
                return cursor.fetchone()
            return cursor.fetchall()
        except:
            print('SQL执行失败，执行语句为:{}'.format(sql))

    def close(self):
        '''关闭数据库连接'''
        self.conn.close()
        # self.cursor().close()

if __name__ == '__main__':
    pass

#'UPDATE `member` SET `pwd`='123' WHERE (`id`='10213227');'
#'SELECT  * FROM futureloan.member LIMIT 10;'