import json
import pytest
import requests
from middleware.middle import MidHandler

data = MidHandler.excel.read("add")
@pytest.mark.parametrize("info",data)
def test_add(info,admin_login):
    '''新增项目用例'''
    #替换member_id
    headers = json.loads(info['headers'])
    headers['Authorization'] = admin_login["token"]
    if "#member_id#" in str(info["json"]):
        info["json"]= info["json"].replace("#member_id#",str(admin_login["id"]))
    resp= requests.request(url=MidHandler.yaml_config['host']+info['url'],
                           method=info['method'],
                           json=json.loads(info['json']),
                           headers=headers
                           )

    resp_json = resp.json()
    assert resp_json['code'] == info['expected']
if __name__ == '__main__':
    pytest.main()