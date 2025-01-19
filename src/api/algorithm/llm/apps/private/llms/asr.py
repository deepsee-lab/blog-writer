# -*- coding: utf-8 -*-
from loguru import logger
from apps.private.llms.utils.get_llm_client import get_llm_client


def asr(file, model, inference_service='ollama', timeout=60):
    client = get_llm_client(inference_service, use_openai_client=True)
    with open(file, "rb") as audio_file:
        res = client.audio.transcriptions.create(
            model=model,
            file=audio_file,
        )
        logger.info(f'res: {res}')
        return res.text
