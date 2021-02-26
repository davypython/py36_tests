import json
import os

import pytest
import requests



# 数据获取
from middleware.middle import MidHandler

data = MidHandler.excel.read('login')

# yaml测试账号拼接

test_mobile_phone = MidHandler.safe_config["investor_user"]['mobile_phone']
test_pwd = MidHandler.safe_config["investor_user"]['pwd']
@pytest.mark.parametrize('info',data)
def test_login(info):
    info = json.dumps(info)
    # 完成替换操作
    info = MidHandler.replace_data(info)
    # 在转化成字典
    info = json.loads(info)
    expected = json.loads(info['expected'])
    # 当读取表格内容有#new_phone# 执行随机号码的替换
    resp = requests.request(
        method=info['method'],
        url=MidHandler.yaml_config['host'] + info['url'],
        json=json.loads(info['json']),
        headers=json.loads(info['headers']))
    # 当msg == expected
    resp_json = resp.json()
    try:
        for key,value in expected.items():
            assert resp_json[key] == value
    except AssertionError as e:
        MidHandler.logger.error('用例执行失败{}'.format(e))
        raise e


if __name__ == '__main__':

    pytest.main(['-W','ignore:Module already imported:pytest.PytestWarning'])