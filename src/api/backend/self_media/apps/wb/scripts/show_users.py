import os
from dotenv import load_dotenv
import requests

load_dotenv()

url = 'https://api.weibo.com/2/users/show.json'
data_json = {
    'access_token': os.getenv("access_token"),
}
res = requests.get(url, data=data_json)
print(res.json())
