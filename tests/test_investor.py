import json
import pytest
import requests
from middleware.middle import MidHandler
from jsonpath import jsonpath
data= MidHandler.excel.read('invest')
@pytest.mark.parametrize('info',data)
def test_investor(info):
    # 要保证替换成功，excel当中#investor_phone# 必须和属性名一致
    # 先转化为json字符串
    info=json.dumps(info)
    # 完成替换操作
    info=MidHandler.replace_data(info)
    # 在转化成字典
    info=json.loads(info)
    expected = json.loads(info['expected'])
    resp = requests.request(url=MidHandler.yaml_config["host"]+info["url"],
                            method=info["method"],
                            headers=json.loads(info['headers']),
                            json=json.loads(info['json']))

    resp_json=resp.json()
    for key, e_value in expected.items():
        assert resp_json[key] == e_value
    if info['extractor']:
        extractors=json.loads(info['extractor'])
        for mid_prop,jsonpath_exp in extractors.items():
            #value='token'
            value = jsonpath(resp_json,jsonpath_exp)[0]
            setattr(MidHandler,mid_prop,value)
if __name__ == '__main__':
    pytest.main()