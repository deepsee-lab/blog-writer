import os
import requests


def upload(bucket_name, localfile, expire_time):
    url = 'http://127.0.0.1:6070/upload'
    json_data = {
        "bucket_name": bucket_name,
        "localfile": localfile,
        "expire_time": expire_time
    }
    res = requests.post(url, json=json_data)
    return res.json()['data']['url']


def run():
    bucket_name = 'ca-test'
    localfile = 'demo.txt'
    # localfile = 'demo.mp4'
    localfile = os.path.abspath(localfile)
    expire_time = 3600
    res = upload(bucket_name, localfile, expire_time)
    print(res)


if __name__ == '__main__':
    run()
