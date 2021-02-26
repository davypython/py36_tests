import json

import pytest,requests


from middleware.middle import MidHandler

data = MidHandler.excel.read('register')
@pytest.mark.parametrize('info',data)
def test_register(info):
    # 当读取表格内容有#new_phone# 执行随机号码的替换
    # if "#new_phone#" in info['json']:
    #     phone_number = MidHandler.random_number_1()
    #     info['json']=str(info['json']).replace("#new_phone#",phone_number)
    # 要保证替换成功，excel当中#investor_phone# 必须和属性名一致
    # 先转化为json字符串
    MidHandler.new_phone = MidHandler.random_number_1()
    info = json.dumps(info)
    # 完成替换操作
    info = MidHandler.replace_data(info)
    # 在转化成字典
    info = json.loads(info)
    expected = json.loads(info['expected'])
    resp = requests.request(
        method=info['method'],
        url=MidHandler.yaml_config['host']+info['url'],
        headers=json.loads(info['headers']),
        json=json.loads(info['json']))
    resp_json = resp.json()
    for key,value in expected.items():
        assert resp_json[key] == value
if __name__ == '__main__':

    pytest.main()