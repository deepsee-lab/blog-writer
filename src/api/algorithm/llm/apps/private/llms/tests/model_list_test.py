from pprint import pprint
from loguru import logger
from apps.private.llms.model_list import get_model_list


def run():
    inference_service_list = [
        'ollama',
        'xinference',
        'one-api',
        'openai',
    ]
    for inference_service in inference_service_list:
        logger.info(f'inference_service: {inference_service}')

        result = get_model_list(inference_service)
        logger.info(f'result: {result}')
        pprint(result)

        logger.info('-' * 80)


if __name__ == '__main__':
    run()
