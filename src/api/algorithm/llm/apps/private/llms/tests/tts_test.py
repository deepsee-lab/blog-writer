import os
import pandas as pd
from loguru import logger
from apps.private.llms.tts import tts


def run():
    filename = 'demo'
    text = '你好，欢迎使用文字转语音ChatTTS，很棒！'

    inference_service_list = [
        'openai',
        'xinference',
    ]

    logger.info(f'text: {text}')

    for inference_service in inference_service_list:
        logger.info(f'inference_service: {inference_service}')

        if inference_service == 'openai':
            model = "tts-1-hd-1106"
            use_openai_client = True
            voice = "echo"
        else:

            model = "ChatTTS"
            # True, False
            use_openai_client = True
            df = pd.read_csv(os.path.join(os.path.dirname(__file__), "evaluation_results.csv"))
            emb_data_2155 = df[df['seed_id'] == 'seed_2155'].iloc[0]["emb_data"]
            voice = emb_data_2155

        logger.info(f'model: {model}')
        logger.info(f'use_openai_client: {use_openai_client}')

        filename = f'{filename}_{inference_service}'

        result = tts(filename=filename, text=text, voice=voice, model=model, use_openai_client=use_openai_client,
                     inference_service=inference_service)

        logger.info('result: {}'.format(result))


if __name__ == '__main__':
    run()
