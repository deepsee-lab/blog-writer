from loguru import logger
from apps.private.llms.image_generation import image_generation


def run():
    filename = 'dog'
    model = "FLUX.1-dev"
    prompt = "A dog holding a sign that says hello world"
    inference_service_list = [
        # 'openai',
        'one-api',
        'xinference',
    ]
    for inference_service in inference_service_list:
        if inference_service == 'openai':
            # dall-e-3
            # dall-e-2
            output_file = image_generation(filename, 'dall-e-2', prompt, inference_service)
        else:
            output_file = image_generation(filename, model, prompt, inference_service)

        logger.info('output_file: {}'.format(output_file))


if __name__ == '__main__':
    run()
