# -*- coding: utf-8 -*-
# Standard library imports.
import os
import base64
#
from loguru import logger
# Local application/library specific imports.
from apps.private.llms.utils.get_llm_client import get_llm_client
from apps.private.llms.config_llm_client.config import OUTPUT_DATA_DIR


def video_generation(filename, model, prompt, inference_service='xinference'):
    client = get_llm_client(inference_service, use_openai_client=False)
    model = client.get_model(model)
    res = model.text_to_video(prompt)
    output_dir = os.path.join(OUTPUT_DATA_DIR, 'llm', 'video')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f'{filename}.mp4')
    output_file = os.path.abspath(output_file)
    with open(output_file, 'wb') as f:
        f.write(base64.b64decode(res.get('data', [])[0].get('b64_json')))
    return output_file
