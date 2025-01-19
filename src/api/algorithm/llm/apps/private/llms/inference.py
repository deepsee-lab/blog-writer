# -*- coding: utf-8 -*-
from apps.private.llms.utils.get_llm_client import get_llm_client


def inf(messages, model, max_tokens=4096, stream=False, temperature=0.8, timeout=60, inference_service='ollama'):
    client = get_llm_client(inference_service, use_openai_client=True)
    completion = client.chat.completions.create(
        messages=messages,
        model=model,
        max_tokens=max_tokens,
        stream=stream,
        temperature=temperature,
        timeout=timeout,
    )
    if stream:
        # TODO: not supported.
        # for chunk in completion:
        #     print(chunk.choices[0].delta)
        return None
    else:
        return vars(completion.choices[0].message)
