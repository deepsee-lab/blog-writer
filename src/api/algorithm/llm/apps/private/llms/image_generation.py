# -*- coding: utf-8 -*-
# Standard library imports.
import os
import base64
# Local application/library specific imports.
from apps.private.llms.utils.get_llm_client import get_llm_client
from apps.private.llms.config_llm_client.config import OUTPUT_DATA_DIR


def image_generation(filename, model, prompt, inference_service='xinference', response_format='b64_json'):
    client = get_llm_client(inference_service, use_openai_client=True)
    # response_format: ["url", "b64_json"]
    if response_format == 'b64_json':
        res = client.images.generate(
            model=model,
            prompt=prompt,
            response_format=response_format
        )
        output_dir = os.path.join(OUTPUT_DATA_DIR, 'llm', 'image')
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, f'{filename}.png')
        output_file = os.path.abspath(output_file)
        with open(output_file, 'wb') as f:
            f.write(base64.b64decode(res.data[0].b64_json))
    else:
        output_file = None
    return output_file
