import requests

url = 'http://127.0.0.1:4010/'
res = requests.get(url)
print(res.json())
