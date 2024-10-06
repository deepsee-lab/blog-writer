# -*- coding: utf-8 -*-
import os
from qiniu import Auth, put_file, etag
import qiniu.config
from dotenv import load_dotenv
from uuid import uuid4
from pathlib import Path

load_dotenv()


def upload_file(bucket_name, localfile, expire_time):
    access_key = os.getenv('QINIU_ACCESS_KEY')
    secret_key = os.getenv('QINIU_SECRET_KEY')

    # 上传后保存的文件名
    filename = str(uuid4()).replace('-', '')
    suffix = Path(localfile).suffix[1:]
    key = '{}/{}.{}'.format(suffix, filename, suffix)

    # 构建鉴权对象
    q = Auth(access_key, secret_key)

    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key, expire_time)

    ret, info = put_file(token, key, localfile, version='v2')

    assert ret['key'] == key
    assert ret['hash'] == etag(localfile)

    domain = os.getenv('QINIU_DOMAIN')
    url = 'http://{}/{}'.format(domain, key)

    return url


def run():
    # 要上传的空间
    bucket_name = 'wwa-test'
    # 要上传文件的本地路径
    # localfile = 'demo.txt'
    localfile = 'demo.mp4'
    # 过期时间
    expire_time = 3600 * 4

    res = upload_file(bucket_name, localfile, expire_time)
    print(res)


if __name__ == '__main__':
    run()
