import os
from loguru import logger
from apps.private.llms.utils.get_llm_client import get_llm_client
from apps.private.llms.config_llm_client.config import OUTPUT_DATA_DIR


def tts(filename, text, voice, model, inference_service='ollama', use_openai_client=False, timeout=60):
    client = get_llm_client(inference_service, use_openai_client=use_openai_client)
    if use_openai_client is True:
        res = client.audio.speech.create(
            model=model,
            input=text,
            voice=voice
        )
        resp_bytes = res.read()
    else:
        model = client.get_model(model)
        resp_bytes = model.speech(
            voice=voice,
            input=text
        )
    output_dir = os.path.join(OUTPUT_DATA_DIR, 'llm', 'tts')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f'{filename}.wav')
    output_file = os.path.abspath(output_file)
    with open(output_file, 'wb') as f:
        f.write(resp_bytes)
    return output_file
