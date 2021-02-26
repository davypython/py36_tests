'''
提现用例设计
1.导入表格数据DDT
2.定义提现函数
把headers替换字典格式添加 Authorization：token（使用json.loads）
替换json里member_id标签 （从login：id夹具获取）
替换json里wrong_member （login：id+1）
发请求前连接数据库获取：用户余额
发请求
断言 code =excepted
校验数据 如果code ==0
1.连接数据库获取用户余额 2.获取请求的info[json]（提现金额）
断言 请求前余额+提现余额 = 请求后余额
'''
import json
from decimal import Decimal
import pytest
import requests

# 获取表格数据
from middleware.middle import MidHandler


data = MidHandler.excel.read('withdraw')
@pytest.mark.parametrize('info',data)
def test_withdraw(info,loan_login,db):
    '''提现用例'''
    headers = json.loads(info['headers'])
    headers['Authorization']=loan_login['token']
    if "#member_id#" in info["json"]:
        info["json"]=info["json"].replace("#member_id#",str(loan_login["id"]))
    if "*wrong_member_id*" in info["json"]:
        info["json"]= info["json"].replace("*wrong_member_id*",str(loan_login["id"]+1))
    if "#beyond_balace#" in info["json"]:
        a_sql = "select leave_amount from member where id={}".format(loan_login["id"])
        amount_db=MidHandler.db_class()
        a_result = amount_db.connect(a_sql,fetchone=True)
        beyond_balace = a_result['leave_amount']
        info["json"] = info["json"].replace("#beyond_balace#",str(beyond_balace+1))



    sql = "select leave_amount from member where id={}".format(loan_login["id"])
    result = db.connect(sql,fetchone=True)
    before_money = result['leave_amount']
    resp = requests.request(method=info["method"],
                            url=MidHandler.yaml_config['host']+info['url'],
                            headers=headers,
                            json=json.loads(info["json"]))
    resp=resp.json()
    try:
        assert resp["code"] == info['expected']
    except AssertionError as e:
        MidHandler.logger.error('用例失败,{}'.format(e))
    # 数据库校验
    if resp["code"] == 0:
        result = db.connect(sql,fetchone=True)
        atfer_money = result['leave_amount']
        mone = json.loads(info["json"])
        money = Decimal(str(mone['amount']))
        try:
            assert before_money+money == atfer_money
        except AssertionError as e:
            MidHandler.logger.error('用例失败'.format(e))
if __name__ == '__main__':
    pytest.main()