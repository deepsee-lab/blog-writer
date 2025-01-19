import json
import os

import requests

from dotenv import load_dotenv

load_dotenv()


def uploadimg(access_token, file_path):
    # 定义 API 的 URL
    url = f'https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token={access_token}'

    # 准备文件字典，这里的 'media' 对应于 curl 中的 -F 参数
    files = {'media': open(file_path, 'rb')}

    # 发送 POST 请求
    response = requests.post(url, files=files)

    # 关闭文件
    files['media'].close()

    # 响应内容
    result = response.json()

    return result


def add_material_img(access_token, file_path):
    # 定义 API 的 URL
    url = f'https://api.weixin.qq.com/cgi-bin/material/add_material?type=image&access_token={access_token}'

    # 准备文件字典，这里的 'media' 对应于 curl 中的 -F 参数
    files = {'media': open(file_path, 'rb')}

    # 发送 POST 请求
    response = requests.post(url, files=files)

    # 关闭文件
    files['media'].close()

    # 响应内容
    result = response.json()

    return result


def add_material_video(access_token, file_path, title, introduction):
    # 定义 API 的 URL
    url = f'https://api.weixin.qq.com/cgi-bin/material/add_material?type=image&access_token={access_token}'

    description = {
        'title': title,
        'introduction': introduction
    }
    # 准备文件字典，这里的 'media' 对应于 curl 中的 -F 参数
    files = {
        'media': open(file_path, 'rb'),
        'description': (None, json.dumps(description, ensure_ascii=False))
    }

    # 发送 POST 请求
    response = requests.post(url, files=files)

    # 关闭文件
    files['media'].close()

    # 响应内容
    result = response.json()

    return result


def run():
    # 设置你的访问令牌和文件路径
    access_token = os.getenv('access_token')

    # file_path = 'logo.png'
    # result = uploadimg(access_token, file_path)
    # result = add_material_img(access_token, file_path)

    file_path = 'demo.mp4'
    title = '标题'
    introduction = '介绍'
    result = add_material_video(access_token, file_path, title, introduction)

    print('result: {}'.format(result))


if __name__ == '__main__':
    run()
