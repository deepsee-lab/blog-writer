import requests


def ch2en(text):
    url = 'http://127.0.0.1:6010/translation/ByteDance/ch2en'
    json_data = {
        "text": text,
    }
    res = requests.post(url, json=json_data)
    return res.json()['data']['result']


def en2ch(text):
    url = 'http://127.0.0.1:6010/translation/ByteDance/en2ch'
    json_data = {
        "text": text,
    }
    res = requests.post(url, json=json_data)
    return res.json()['data']['result']
