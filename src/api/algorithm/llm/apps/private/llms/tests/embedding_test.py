from loguru import logger
from apps.private.llms.embedding import get_embedding_list


def run():
    model = 'bge-base-zh-v1.5'
    text_list = ['你好', 'hello']
    inference_service_list = [
        # 'openai',
        'ollama',
        'one-api',
        'xinference',
    ]
    for inference_service in inference_service_list:
        if inference_service == 'openai':
            # text-embedding-3-large
            # text-embedding-ada-002
            # text-embedding-3-small
            result = get_embedding_list('text-embedding-ada-002', text_list, inference_service)
        elif inference_service in ['ollama']:
            result = get_embedding_list('nomic-embed-text:137m-v1.5-fp16', text_list, inference_service)
        else:
            result = get_embedding_list(model, text_list, inference_service)

        logger.info('result: {}'.format(result))


if __name__ == '__main__':
    run()
