'''
充值用例设计
1.前置条件准备：获取登录成功
2.取到 鉴权、token 、leave_amount
3.充值用例中拼接
数据校验：
1.在请求前获取数据库余额
2.请求后获取数据库余额
3.断言 充值前余额+ 充值金额 == 充值后余额
'''

import json
from decimal import Decimal
import pytest
import requests
from middleware.middle import MidHandler


data = MidHandler.excel.read('recharge')


@pytest.mark.parametrize('info', data)
def test_recharge(info, loan_login,db):
    # 先要替换
    if "#member_id#" in info["json"]:
        info["json"] = info["json"].replace('#member_id#', str(loan_login['id']))
    '''
    序列化和反序列号
    json.loads =json格式字符串转化成python当中字典
    json.dumps =python当中字典转化成json格式字符串
    '''
    headers = json.loads(info["headers"])
    headers['Authorization'] = loan_login['token']
    if "*wrong_member_id*" in info["json"]:
        info["json"] = info["json"].replace('*wrong_member_id*', str(loan_login['id'] + 1))
    # 请求前的数据库 余额
    sql= 'select leave_amount from member where id={}'.format(str(loan_login['id']))
    result=db.connect(sql,fetchone=True)
    money_before = result['leave_amount']
    resp = requests.request(url=MidHandler.yaml_config['host'] + info['url'],
                            method=info['method'],
                            headers=headers,
                            json=json.loads(info['json']))
    try:
        assert resp.json()['code'] == info["expected"]
    except AssertionError as e:
        MidHandler.logger.error('用例执行失败{}'.format(e))
        raise e
    if resp.json()['code'] == 0:
        # 获取充值后余额
        sql = 'select leave_amount from member where id={}'.format(str(loan_login['id']))
        result = db.connect(sql, fetchone=True)
        money_after = result['leave_amount']
        # db.close()
        # 获取充值的钱
        mone=json.loads(info['json'])
        money = Decimal(str(mone['amount']))
        # 断言 充值前钱+充值的钱 = 充值后的余额
        try:
            assert money + money_before == money_after
        except AssertionError as e:
            MidHandler.logger.error('用例失败{}'.format(e))
            raise e



if __name__ == '__main__':
    # sql = 'select leave_amount from member where id=2067;'
    # data = MidHandler.db_class
    # info = data.connect(sql, fetchone=True)
    # print(info)
    pytest.main()