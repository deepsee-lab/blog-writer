from openai import OpenAI
# add log start
import os
import time
from loguru import logger

file_name = '.'.join(os.path.basename(__file__).split('.')[:-1])
log_dir = os.path.join('logs', file_name)
log_file = os.path.join(log_dir, '{time:YYYY-MM-DD}.log')
logger.add(log_file, rotation="00:00", enqueue=True, serialize=False, encoding="utf-8")
# add log end

client = OpenAI(
    base_url='http://localhost:11434/v1/',
    api_key='ollama',  # required but ignored
)


def inf(messages, model, max_tokens=4096, stream=False, temperature=0.8, timeout=60, inference_service='ollama'):
    if inference_service == 'ollama':
        chat_completion = client.chat.completions.create(
            messages=messages,
            model=model,
            max_tokens=max_tokens,
            stream=stream,
            temperature=temperature,
            timeout=timeout,
        )
        result = chat_completion.choices[0].message.content
        return result
    else:
        raise Exception('inference_service not supported')


def run():
    prompt = 'hi'
    messages = [
        {
            'role': 'user',
            'content': prompt,
        }
    ]
    model = 'qwen2:1.5b-instruct-fp16'
    result = inf(messages=messages, model=model)

    logger.debug('prompt: {}'.format(prompt))
    logger.debug('result: {}'.format(result))


if __name__ == '__main__':
    time1 = time.time()

    run()

    time2 = time.time()

    logger.debug(f'total time: {time2 - time1}')
    logger.debug('-' * 40)
