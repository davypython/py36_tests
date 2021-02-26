'''帮助函数'''
import random
from faker import Faker

from middleware.middle import MidHandler


def random_number_1():
    '''随机生成电话'''
    mobile_number='1'+random.choice(['3','5','7','8','9'])
    for i in range(9):
        mobile_number+=str(random.randint(1,9))
    return mobile_number

def random_number_2():
    '''检验手机号是否存在数据库'''
    while True:
        number = Faker(locale='zh_CN')
        mobile_number=number.phone_number()
        sql = 'SELECT mobile_phone FROM member WHRER mobile_phone={};'.format(str(mobile_number))
        db_number = MidHandler.db_class()
        db_num=db_number.connect(sql, fetchone=False)
        db_number.close()
        if db_num :
            MidHandler.logger.info('手机号码已存在')
        else:
            return mobile_number



if __name__ == '__main__':
    print(random_number_2())

