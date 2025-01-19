import urllib.parse
import os
from dotenv import load_dotenv
import requests

load_dotenv()

# 定义必选参数
access_token = os.getenv("access_token")
status = "要发布的微博文本内容"  # 请确保内容不超过140个汉字，如果是长文请设置is_longtext为1
rip = os.getenv("rip")

# 对status进行URLencode
status_encoded = urllib.parse.quote(status)

# 定义可选参数
visible = 0  # 所有人可见
is_longtext = 0  # 不是长文
lat = 0.0  # 默认纬度
long = 0.0  # 默认经度
annotations = '{"key1":"value1","key2":"value2"}'  # 示例元数据

# 构建请求数据
data = {
    "access_token": access_token,
    "status": status_encoded,
    "visible": visible,
    "is_longtext": is_longtext,
    "lat": lat,
    "long": long,
    "annotations": annotations,
    "rip": rip
}

# 发送POST请求
url = "https://api.weibo.com/2/statuses/update.json"
response = requests.post(url, data=data)

# 处理响应
if response.status_code == 200:
    print("微博发布成功")
    print(response.json())
else:
    print("微博发布失败")
    print(response.status_code, response.text)
