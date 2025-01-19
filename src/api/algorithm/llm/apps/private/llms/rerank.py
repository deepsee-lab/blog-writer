# -*- coding: utf-8 -*-
from apps.private.llms.utils.get_llm_client import get_llm_client


def re_rank(model, query, corpus, inference_service):
    client = get_llm_client(inference_service, use_openai_client=False)
    model = client.get_model(model)
    return model.rerank(corpus, query)
