import os
from dotenv import load_dotenv
import requests

load_dotenv()

url = 'https://api.weibo.com/oauth2/authorize'
data_json = {
    'client_id': os.getenv("client_id"),
    'redirect_uri': os.getenv("redirect_uri"),
}
res = requests.get(url, data=data_json)
print(res.json())
