import json

import requests

from common import tools


def requestGet(url):
    ret = requests.get(url)
    if ret.status_code != 200:
        print("请求马甲接口失败，状态不为200,状态码为" + url)
        print("请求马甲接口失败，状态不为200,状态码为" + str(ret.status_code))
        return {}
    else:
        response = json.loads(ret.text)
        if response["code"] != 0:
            print("code:" + str(response["code"]) + "," + response["msg"])
            response = {}
            # friends = friend["data"]

        return response

