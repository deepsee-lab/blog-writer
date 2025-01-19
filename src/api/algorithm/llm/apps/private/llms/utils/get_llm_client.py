# -*- coding: utf-8 -*-


def get_llm_client(inference_service, use_openai_client=True):
    client = None
    if str(inference_service).lower() == 'openai':
        if use_openai_client:
            from apps.private.llms.config_llm_client.config import openai_client_online

            client = openai_client_online
    elif str(inference_service).lower().replace('-', '') == 'oneapi':
        from apps.private.llms.config_llm_client.config import openai_client_one_api

        if use_openai_client:
            client = openai_client_one_api
    elif str(inference_service).lower() == 'ollama':
        from apps.private.llms.config_llm_client.config import openai_client_ollama

        if use_openai_client:
            client = openai_client_ollama
    elif str(inference_service).lower() == 'xinference':
        from apps.private.llms.config_llm_client.config import openai_client_xinference, xinference_client

        if use_openai_client:
            client = openai_client_xinference
        else:
            client = xinference_client
    return client
