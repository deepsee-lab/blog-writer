# -*- coding: utf-8 -*-
# Standard library imports.
import os
# Related third party imports.
from loguru import logger
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

one_api_client = OpenAI(
    base_url=os.getenv('ONE_API_BASE'),
    api_key=os.getenv('ONE_API_KEY'),
)


def inf(messages, model, max_tokens=4096, stream=False, temperature=0.8, timeout=60):
    completion = one_api_client.chat.completions.create(
        messages=messages,
        model=model,
        max_tokens=max_tokens,
        stream=stream,
        temperature=temperature,
        timeout=timeout,
    )
    if stream:
        # TODO: 尚未支持
        # for chunk in completion:
        #     print(chunk.choices[0].delta)
        return None
    else:
        return vars(completion.choices[0].message)


def get_embedding_list(model, sentences):
    response = one_api_client.embeddings.create(
        model=model,
        input=sentences,
        encoding_format="float"
    )
    return [item.embedding for item in response.data]


def run_inf_llm():
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who won the world series in 2020?"},
        {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
        {"role": "user", "content": "Where was it played?"}
    ]
    result = inf(messages=messages, model='qwen2.5:0.5b-instruct-fp16')

    logger.info('result: {}'.format(result))


def run_inf_lvm():
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "What'\''s in this image?"
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://bkimg.cdn.bcebos.com/pic/b3b7d0a20cf431adcbef4b5f576ebbaf2edda3cc3207"
                    }
                }
            ]
        }
    ]
    result = inf(messages=messages, model='qwen-vl-chat')

    logger.info('result: {}'.format(result))


def run_get_embedding_list():
    model = 'bge-base-zh-v1.5'
    text_list = ['你好', '您好']
    result = get_embedding_list(model, text_list)

    logger.info('result: {}'.format(result))


def run():
    run_inf_llm()
    run_inf_lvm()
    run_get_embedding_list()


if __name__ == '__main__':
    run()
