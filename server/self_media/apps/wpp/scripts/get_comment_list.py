import os
import requests
from dotenv import load_dotenv

load_dotenv()

url = 'https://api.weixin.qq.com/cgi-bin/comment/list?access_token={}'.format(os.getenv('access_token'))
# 参数说明
# 参数	是否必须	类型	说明
# msg_data_id	是	Uint32	群发返回的msg_data_id
# index	否	Uint32	多图文时，用来指定第几篇图文，从0开始，不带默认返回该msg_data_id的第一篇图文
# begin	是	Uint32	起始位置
# count	是	Uint32	获取数目（>=50会被拒绝）
# type	是	Uint32	type=0 普通评论&精选评论 type=1 普通评论 type=2 精选评论
MSG_DATA_ID = 'XXXX'
INDEX = 0
BEGIN = 0
COUNT = 49
MY_TYPE = 0
json_data = {
    "msg_data_id": MSG_DATA_ID,
    "index": INDEX,
    "begin": BEGIN,
    "count": COUNT,
    "type": MY_TYPE
}
resp = requests.post(url, json=json_data)
print(resp.json())
