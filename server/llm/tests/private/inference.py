import requests

url = 'http://127.0.0.1:4010/private/inference'
json_data = {
    "messages": [
        "string"
    ],
    "inference_service": "ollama",
    "model": "qwen2:1.5b-instruct-fp16",
    "max_tokens": 4096,
    "stream": False,
    "temperature": 0.8,
    "timeout": 60
}
res = requests.post(url, json=json_data)
print(res.json())
