from loguru import logger
from apps.private.llms.asr import asr


def run():
    file = 'asr_sample.wav'
    model = "whisper-large-v3"
    inference_service_list = [
        'openai',
        'xinference',
    ]

    logger.info(f'file: {file}')
    logger.info(f'model: {model}')

    for inference_service in inference_service_list:
        logger.info(f'inference_service: {inference_service}')

        if inference_service == 'openai':
            result = asr(file, 'whisper-1', inference_service)
        else:
            result = asr(file, model, inference_service)

        logger.info('result: {}'.format(result))


if __name__ == '__main__':
    run()
