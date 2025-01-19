import requests


def get_retrieve_inference(kb_id, query, top_k, output_fields):
    url = 'http://127.0.0.1:6020/vector/search'
    json_data = {
        "kb_id": kb_id,
        "query": query,
        "top_k": top_k,
        "output_fields": output_fields
    }
    res = requests.post(url, json=json_data)
    return res.json()['data']['results']


def get_llm_inference(inference_service, messages, model, max_tokens, stream, temperature, timeout):
    url = 'http://127.0.0.1:4010/private/inference'
    json_data = {
        "messages": messages,
        "inference_service": inference_service,
        "model": model,
        "max_tokens": max_tokens,
        "stream": stream,
        "temperature": temperature,
        "timeout": timeout,
    }
    res = requests.post(url, json=json_data)
    return res.json()['data']['result']


def run():
    json_data = {
        "messages": [
            {
                "role": "user",
                "content": "您好"
            }
        ],
        "inference_service": "ollama",
        "model": "qwen2:1.5b-instruct-fp16",
        "max_tokens": 4096,
        "stream": False,
        "temperature": 0.8,
        "timeout": 60
    }
    get_llm_inference(**json_data)


if __name__ == '__main__':
    run()
