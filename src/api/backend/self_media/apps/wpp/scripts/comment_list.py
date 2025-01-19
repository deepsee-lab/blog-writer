import requests
# add log start
import os
from loguru import logger

file_name = '.'.join(os.path.basename(__file__).split('.')[:-1])
log_dir = os.path.join('logs', file_name)
log_file = os.path.join(log_dir, '{time:YYYY-MM-DD}.log')
logger.add(log_file, rotation="00:00", enqueue=True, serialize=False, encoding="utf-8")
# add log end
from dotenv import load_dotenv

load_dotenv()


def comment_list(access_token, msg_data_id):
    url = r'https://api.weixin.qq.com/cgi-bin/comment/list?access_token={}'.format(access_token)
    # 参数说明
    # 参数	是否必须	类型	说明
    # msg_data_id	是	Uint32	群发返回的msg_data_id
    # index	否	Uint32	多图文时，用来指定第几篇图文，从0开始，不带默认返回该msg_data_id的第一篇图文
    # begin	是	Uint32	起始位置
    # count	是	Uint32	获取数目（>=50会被拒绝）
    # type	是	Uint32	type=0 普通评论&精选评论 type=1 普通评论 type=2 精选评论
    BEGIN = 0
    COUNT = 49
    json_data = {
        "msg_data_id": msg_data_id,
        # "index": INDEX,
        "begin": BEGIN,
        "count": COUNT,
        "type": 0
    }

    resp = requests.post(url, json=json_data)
    result = resp.json()
    return result


def run():
    access_token = os.getenv('access_token')
    msg_data_id = os.getenv('msg_data_id')
    result = comment_list(access_token, msg_data_id)
    logger.info('result: {}'.format(result))


if __name__ == '__main__':
    # need api authorized
    run()
