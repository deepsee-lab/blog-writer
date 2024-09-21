import os
import requests
# add log start
import os
import time
from loguru import logger

file_name = '.'.join(os.path.basename(__file__).split('.')[:-1])
log_dir = os.path.join('logs', file_name)
log_file = os.path.join(log_dir, '{time:YYYY-MM-DD}.log')
logger.add(log_file, rotation="00:00", enqueue=True, serialize=False, encoding="utf-8")
# add log end
from dotenv import load_dotenv

load_dotenv()


def free_publish(access_token, MEDIA_ID):
    url = 'https://api.weixin.qq.com/cgi-bin/freepublish/submit?access_token={}'.format(access_token)
    # 参数说明
    # 参数	是否必须	说明
    # access_token	是	调用接口凭证
    # media_id	是	要发布的草稿的media_id
    json_data = {
        "media_id": MEDIA_ID,
    }
    resp = requests.post(url, json=json_data)
    # 返回参数说明
    # 参数	说明
    # errcode	错误码
    # errmsg	错误信息
    # publish_id	发布任务的id
    # msg_data_id	消息的数据ID
    result = resp.json()
    return result


def run():
    access_token = os.getenv('access_token')
    MEDIA_ID = os.getenv('MEDIA_ID')
    result = free_publish(access_token, MEDIA_ID)
    logger.info('result: {}'.format(result))


if __name__ == '__main__':
    run()
