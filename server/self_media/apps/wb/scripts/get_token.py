import os
from dotenv import load_dotenv
import requests

load_dotenv()

url = 'https://api.weibo.com/oauth2/access_token'
data_json = {
    'client_id': os.getenv("client_id"),
    'client_secret': os.getenv("client_secret"),
    'grant_type': 'authorization_code',
    'code': os.getenv("code"),
    'redirect_uri': os.getenv("redirect_uri"),
}
res = requests.post(url, data=data_json)
print(res.json())
