# -*- coding: utf-8 -*-
# Standard library imports.
import os
import base64
# Related third party imports.
from loguru import logger
from openai import OpenAI
from dotenv import load_dotenv
from xinference_client import RESTfulClient as Client

load_dotenv()

OUTPUT_DATA_DIR = os.getenv('OUTPUT_DATA_DIR')
XINFERENCE_API_BASE = os.getenv('XINFERENCE_API_BASE')
XINFERENCE_API_KEY = os.getenv('XINFERENCE_API_KEY')
openai_client = OpenAI(
    base_url=os.path.join(XINFERENCE_API_BASE, 'v1'),
    api_key=XINFERENCE_API_KEY,
)
xinference_client = Client(XINFERENCE_API_BASE, api_key=XINFERENCE_API_KEY)


def re_rank(model, query, corpus):
    model = xinference_client.get_model(model)
    return model.rerank(corpus, query)


def image_generation(filename, model, prompt, response_format='b64_json'):
    # response_format: ["url", "b64_json"]
    if response_format == 'b64_json':
        res = openai_client.images.generate(
            model=model,
            prompt=prompt,
            response_format=response_format
        )
        output_dir = os.path.join(OUTPUT_DATA_DIR, 'llm', 'image')
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, f'{filename}.png')
        with open(output_file, 'wb') as f:
            f.write(base64.b64decode(res.data[0].b64_json))
    else:
        output_file = None
    return output_file


def run_re_rank():
    model = "bge-reranker-base"
    query = "A man is eating pasta."
    corpus = [
        "A man is eating food.",
        "A man is eating a piece of bread.",
        "The girl is carrying a baby.",
        "A man is riding a horse.",
        "A woman is playing violin."
    ]
    result = re_rank(model, query, corpus)

    logger.info('result: {}'.format(result))


def run_image_generation():
    filename = 'dog'
    model = "FLUX.1-schnell"
    prompt = "A dog holding a sign that says hello world"
    output_file = image_generation(filename, model, prompt)

    logger.info('output_file: {}'.format(output_file))


def run():
    # run_re_rank()
    run_image_generation()


if __name__ == '__main__':
    run()
