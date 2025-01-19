# -*- coding: utf-8 -*-
# Standard library
import os
import json
import time
# Extended library
from volcengine.ApiInfo import ApiInfo
from volcengine.Credentials import Credentials
from volcengine.ServiceInfo import ServiceInfo
from volcengine.base.Service import Service
from dotenv import load_dotenv

load_dotenv()


def trans(text: str, fromLang: str, toLang: str) -> str:
    if fromLang == 'ch':
        fromLang = 'zh'
    if toLang == 'ch':
        toLang = 'zh'

    # https://console.volcengine.com/iam/keymanage/
    k_access_key = os.environ.get('volcengine_k_access_key')
    k_secret_key = os.environ.get('volcengine_k_secret_key')
    k_service_info = \
        ServiceInfo('translate.volcengineapi.com',
                    {'Content-Type': 'application/json'},
                    Credentials(k_access_key, k_secret_key, 'translate', 'cn-north-1'),
                    5,
                    5)
    k_query = {
        'Action': 'TranslateText',
        'Version': '2020-06-01'
    }
    k_api_info = {
        'translate': ApiInfo('POST', '/', k_query, {}, {})
    }
    service = Service(k_service_info, k_api_info)
    body = {
        'TargetLanguage': toLang,
        'TextList': [text],
    }
    res = service.json('translate', {}, json.dumps(body))
    result = json.loads(res).get('TranslationList', [{}])[0].get('Translation', '')
    return result


def run_ch2en(text):
    fromLang = 'ch'  # 原文语种
    toLang = 'en'  # 译文语种
    result = trans(text, fromLang=fromLang, toLang=toLang)
    return result


def run_en2ch(text):
    fromLang = 'en'  # 原文语种
    toLang = 'ch'  # 译文语种
    result = trans(text, fromLang=fromLang, toLang=toLang)
    return result


def run():
    text = """
在开始与其他同学使用 Github 协同工作之前，请确保熟练使用 Github 的协同编程。如果不了解，请先学习该笔记。
    """.strip()
    result = run_ch2en(text)
    print('ch2en: {}'.format(result))

    text = """
Welcome to the weibo-writer-agent wiki!
Wikis provide a place in your repository to lay out the roadmap of your project, show the current status, and document software better, together.
    """.strip()
    result = run_en2ch(text)
    print('en2ch: {}'.format(result))


if __name__ == '__main__':
    t1 = time.time()

    run()

    t2 = time.time()
    print(' time: {:.2f}s'.format(t2 - t1))
