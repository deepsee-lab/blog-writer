# -*- coding: utf-8 -*-
from apps.private.llms.utils.get_llm_client import get_llm_client


def get_model_list(inference_service='ollama'):
    client = get_llm_client(inference_service, use_openai_client=True)
    return sorted([model.id for model in client.models.list().data])
