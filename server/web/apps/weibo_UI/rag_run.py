import requests
from loguru import logger

def vector_model_rag(url,KB_id,top_K,query,type_name,model_select):
    #url = 'http://127.0.0.1:4010/private/inference'
    logger.info('vector_model_rag,kb--id:')
    logger.info(KB_id)
    json_data = {
        "retrieve_only": False,
        "vector_search": True,
        "kb_id": KB_id,
        "top_k": top_K,
        "threshold_value": 0,
        "messages": [
            {
            "role": "user",
            "content": query
            }
        ],
        "inference_service": type_name,
        "model": model_select,
        "max_tokens": 4096,
        "stream": False,
        "temperature": 0.8,
        "timeout": 60
    }
    # 发送请求并存储响应
    response = requests.post(url, json=json_data).json()
    return response

def no_vector_model_rag(url,query,type_name,model_select):
    #url = 'http://127.0.0.1:4010/private/inference'
    json_data = {
            "inference_service": type_name,
            "messages": [
              {
                "role": "user",
                "content": query
              }
            ],
            "model": model_select,
            "max_tokens": 4096,
            "stream": False,
            "temperature": 0.8,
            "timeout": 60
    }
    # 发送请求并存储响应
    response = requests.post(url, json=json_data).json()
    return response

def kb_list():
    url='http://127.0.0.1:6020/vector/kb_list_all'
    # 发送请求并存储响应
    response = requests.get(url).json()
    logger.info(response)
    return response

if __name__ == '__main__':
    url = 'http://127.0.0.1:4010/private/inference'
    KB_id="uuid0000000000000000000000000111"
    top_K=5
    query="种子"
    type_name='ollama'
    model_select='qwen2:1.5b-instruct-fp16'
    answer=vector_model_rag(url,KB_id,top_K,query,type_name,model_select)
    logger.info(answer)