"""
项目审批用例
前置条件（登录和新增项目）
1.添加新增项目id夹具
2.新增项目夹具（调用login夹具，获取memberid）
3.替换memberid，发起请求,获取项目ID loan_id(保存数据)
项目审批用例
1.前置条件（新增项目夹具）
2.通过项目夹具获取的loan_id，替换 #loan_id#，发起请求
"""
import json
import pytest
import requests
from middleware.middle import MidHandler

data= MidHandler.excel.read('audit')
@pytest.mark.parametrize('info',data)
def test_audit(info,add_fun,admin_login):
    headers =json.loads(info['headers'])
    headers['Authorization'] = admin_login["token"]
    if "#loan_id#" in info['json']:
        info["json"]=(info["json"]).replace("#loan_id#",str(add_fun))
    if "#wrong_loan_id#" in info['json']:
        info["json"] = (info["json"]).replace("#loan_id#", str(add_fun+1))
    json_data=json.loads(info['json'])
    resp = requests.request(url=MidHandler.yaml_config["host"]+info["url"],
                            method=info["method"],
                            json=json_data,
                            headers=headers)
    resp_json=resp.json()
    expected = json.loads(info["expected"])
    # 第一版 多值断言 直接多断言code 和msg
    # assert resp_json["code"] == expected["code"]
    # assert resp_json["msg"] == expected["msg"]
    # 第二版 多值断言 for循环 expected的 key和value 对比响应结果key和请求表格里预期结果是否相等
    for key,value in expected.items():
        assert resp_json[key] == value
if __name__ == '__main__':
    pytest.main()