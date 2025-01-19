# -*- coding: utf-8 -*-
from apps.private.llms.utils.get_llm_client import get_llm_client


def get_embedding_list(model, sentences, inference_service='ollama'):
    client = get_llm_client(inference_service, use_openai_client=True)
    response = client.embeddings.create(
        model=model,
        input=sentences,
        encoding_format="float",
    )
    return [item.embedding for item in response.data]
