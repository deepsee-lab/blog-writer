import time
from loguru import logger
from apps.private.llms.inference import inf


def run_llm_inference():
    prompt = 'hi'
    messages = [
        {
            'role': 'user',
            'content': prompt,
        }
    ]
    model = 'qwen2.5:0.5b-instruct-q8_0'
    inference_service_list = [
        'openai',
        # 'ollama',
        # 'one-api',
        # 'xinference',
    ]
    for inference_service in inference_service_list:
        if inference_service == 'openai':
            # gpt-4-32k
            # o1-preview
            # gpt-4-turbo
            # gpt-4o
            # o1-mini
            # gpt-3.5-turbo
            # gpt-4o-mini
            result = inf(messages=messages, model='gpt-3.5-turbo', inference_service=inference_service)
        else:
            result = inf(messages=messages, model=model, inference_service=inference_service)

        logger.info('prompt: {}'.format(prompt))
        logger.info('result: {}'.format(result))


def run_lvm_inference():
    prompt = "What is in this image?"
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://bkimg.cdn.bcebos.com/pic/b3b7d0a20cf431adcbef4b5f576ebbaf2edda3cc3207"
                    }
                },
                {
                    "type": "text",
                    "text": prompt
                }
            ]
        }
    ]
    model = 'MiniCPM-V-2.6-8B'
    inference_service_list = [
        'openai',
        # 'ollama',
        # 'one-api',
        # 'xinference',
    ]
    for inference_service in inference_service_list:
        if inference_service == 'openai':
            # gpt-4o
            # gpt-4o-mini
            result = inf(messages=messages, model='gpt-4o', inference_service=inference_service)
        else:
            result = inf(messages=messages, model=model, inference_service=inference_service)

        logger.info('prompt: {}'.format(prompt))
        logger.info('result: {}'.format(result))


def run():
    run_llm_inference()
    run_lvm_inference()


if __name__ == '__main__':
    time1 = time.time()

    run()

    time2 = time.time()

    logger.info(f'total time: {time2 - time1}')
    logger.info('-' * 40)
