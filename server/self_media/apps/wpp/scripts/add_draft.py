import json
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
import datetime
from dotenv import load_dotenv

load_dotenv()


def add_draft(access_token, title, author, digest, content, content_source_url, thumb_media_id, need_open_comment,
              only_fans_can_comment):
    url = 'https://api.weixin.qq.com/cgi-bin/draft/add?access_token={}'.format(access_token)
    # 请求参数说明
    # 参数	是否必须	说明
    # title	是	标题
    # author	否	作者
    # digest	否	图文消息的摘要，仅有单图文消息才有摘要，多图文此处为空。如果本字段为没有填写，则默认抓取正文前54个字。
    # content	是	图文消息的具体内容，支持HTML标签，必须少于2万字符，小于1M，且此处会去除JS,涉及图片url必须来源 "上传图文消息内的图片获取URL"接口获取。外部图片url将被过滤。
    # content_source_url	否	图文消息的原文地址，即点击“阅读原文”后的URL
    # thumb_media_id	是	图文消息的封面图片素材id（必须是永久MediaID）
    # need_open_comment	否	Uint32 是否打开评论，0不打开(默认)，1打开
    # only_fans_can_comment	否	Uint32 是否粉丝才可评论，0所有人可评论(默认)，1粉丝才可评论
    # pic_crop_235_1	否	封面裁剪为2.35:1规格的坐标字段。以原始图片（thumb_media_id）左上角（0,0），右下角（1,1）建立平面坐标系，经过裁剪后的图片，其左上角所在的坐标即为（X1,Y1）,右下角所在的坐标则为（X2,Y2），用分隔符_拼接为X1_Y1_X2_Y2，每个坐标值的精度为不超过小数点后6位数字。示例见下图，图中(X1,Y1) 等于（0.1945,0）,(X2,Y2)等于（1,0.5236），所以请求参数值为0.1945_0_1_0.5236。
    # pic_crop_1_1	否	封面裁剪为1:1规格的坐标字段，裁剪原理同pic_crop_235_1，裁剪后的图片必须符合规格要求。
    json_data = {
        "articles": [
            {
                "title": title,
                "author": author,
                "digest": digest,
                "content": content,
                "content_source_url": content_source_url,
                "thumb_media_id": thumb_media_id,
                "need_open_comment": need_open_comment,
                "only_fans_can_comment": only_fans_can_comment,
                # "pic_crop_235_1": pic_crop_235_1,
                # "pic_crop_1_1": pic_crop_1_1
            }
            # //若新增的是多图文素材，则此处应还有几段articles结构
        ]
    }
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    res = requests.post(url, data=json.dumps(json_data, ensure_ascii=False), headers=headers)
    result = res.json()
    return result


def run():
    access_token = os.getenv('access_token')

    title = 'title_{}'.format(str(datetime.datetime.now())[:19].replace(' ', '_').replace(':', '-'))

    logger.info('title: {}'.format(title))

    author = 'author'
    digest = 'digest'
    # file = 'files/article.html'
    # with open(file, 'r', encoding='utf-8') as f:
    #     CONTENT = f.read()
    content = 'CONTENT is 正文'

    logger.info('content: {}'.format(content))

    content_source_url = None
    thumb_media_id = os.getenv('THUMB_MEDIA_ID')
    pic_crop_235_1 = None
    pic_crop_1_1 = None

    need_open_comment = 1
    only_fans_can_comment = 0

    result = add_draft(
        access_token,
        title,
        author,
        digest,
        content,
        content_source_url,
        thumb_media_id,
        need_open_comment,
        only_fans_can_comment
    )
    logger.info('result: {}'.format(result))


if __name__ == '__main__':
    run()
