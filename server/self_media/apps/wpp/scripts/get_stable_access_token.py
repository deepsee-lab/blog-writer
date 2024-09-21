import os
import requests
from dotenv import load_dotenv

load_dotenv()


def get_stable_access_token(appid, secret):
    # 确保访问ip在白名单里面
    url = 'https://api.weixin.qq.com/cgi-bin/stable_token'
    json_data = {
        "grant_type": "client_credential",
        "appid": appid,
        "secret": secret,
    }
    resp = requests.post(url, json=json_data)
    return resp.json()


def run():
    appid = os.getenv('appid')
    secret = os.getenv('secret')
    result = get_stable_access_token(appid, secret)
    print(result)


if __name__ == '__main__':
    run()
