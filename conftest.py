
import requests
from jsonpath import jsonpath
import pytest
from middleware.middle import MidHandler

def login_fuc(phone,pwd):
    user = {
        "mobile_phone": phone,
        "pwd": pwd
    }
    resp = requests.request(method='POST',
                            url=MidHandler.yaml_config['host'] + '/member/login',
                            headers={"X-Lemonban-Media-Type": "lemonban.v2"},
                            json=user
                            )
    resp_json = resp.json()

    token = jsonpath(resp_json, '$..token')[0]
    id = jsonpath(resp_json, '$..id')[0]
    token_type = jsonpath(resp_json, '$..token_type')[0]
    leave_amount = jsonpath(resp_json, '$..leave_amount')[0]
    token = " ".join([token_type, token])
    return {"id": id,
            "token": token,
            "leave_amount": leave_amount}
@pytest.fixture()
def loan_login ():
    # 获取登录账号
    user= {
        "mobile_phone":MidHandler.safe_config["loan_user"]["mobile_phone"],
        "pwd" : MidHandler.safe_config["loan_user"]['pwd']
    }

    return login_fuc(user["mobile_phone"],user["pwd"])


@pytest.fixture()
def admin_login():
    # 获取登录账号
    user= {
        "mobile_phone":MidHandler.safe_config["admin_user"]["mobile_phone"],
        "pwd" : MidHandler.safe_config["admin_user"]['pwd']
    }
    return login_fuc(user["mobile_phone"],user["pwd"])



@pytest.fixture()
def add_fun(loan_login):
    '''新增项目用例'''
    headers = {"X-Lemonban-Media-Type":"lemonban.v2",
               "Authorization":loan_login['token']}
    data={"member_id":loan_login['id'],
          "title":"报名 python 全栈自动化课",
          "amount":6300.00,
          "loan_rate":12.0,
          "loan_term":12,
          "loan_date_type":1,
          "bidding_days":5}
    resp= requests.request(url=MidHandler.yaml_config['host']+'/loan/add',
                           method='POST',
                           json=data,
                           headers=headers)
    resp_json = resp.json()
    loan_id = jsonpath(resp_json, '$..id')[0]
    return loan_id





@pytest.fixture()
def db():
    '''管理数据库模块'''
    db_conn = MidHandler.db_class()
    yield db_conn
    db_conn.close()




if __name__ == '__main__':
    pass