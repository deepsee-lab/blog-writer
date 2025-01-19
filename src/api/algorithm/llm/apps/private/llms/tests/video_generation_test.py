from loguru import logger
from apps.private.llms.video_generation import video_generation


def run():
    filename = 'ship'
    model = "CogVideoX-2b"
    prompt = "A detailed wooden toy ship with intricately carved masts and sails is seen gliding smoothly over a plush, blue carpet that mimics the waves of the sea. The ship's hull is painted a rich brown, with tiny windows. The carpet, soft and textured, provides a perfect backdrop, resembling an oceanic expanse. Surrounding the ship are various other toys and children's items, hinting at a playful environment. The scene captures the innocence and imagination of childhood, with the toy ship's journey symbolizing endless adventures in a whimsical, indoor setting."
    inference_service_list = [
        'xinference',
    ]
    for inference_service in inference_service_list:
        output_file = video_generation(filename, model, prompt, inference_service)

        logger.info('output_file: {}'.format(output_file))


if __name__ == '__main__':
    run()
