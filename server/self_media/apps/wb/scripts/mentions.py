import os
from dotenv import load_dotenv
import requests

load_dotenv()

url = r'https://api.weibo.com/2/statuses/mentions.json'
json_data = {
    'access_token': os.getenv("access_token"),
}
res = requests.get(url, json=json_data)
print(res)
print(res.json())
