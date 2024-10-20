import requests
from loguru import logger
from apps.weibo_UI.models import weibo_Model_setting

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

def no_vector_model_rag(url,query):
    #url = 'http://127.0.0.1:4010/private/inference'
    '''
    Type_item: Mapped[str] = mapped_column(db.String, nullable=False)
    Model_item: Mapped[str] = mapped_column(db.String, nullable=False)
    Top_K: Mapped[str] = mapped_column(db.String, nullable=False)
    Temprature: Mapped[str] = mapped_column(db.String, nullable=False)
    max_time: Mapped[str] = mapped_column(db.String, nullable=False)'''
    item_list = weibo_Model_setting.query.all()
    item_latest=item_list[-1]
    Type_item=item_latest.Type_item
    Model_item=item_latest.Model_item
    #Top_K=item_latest['Top_K']
    Temprature=item_latest.Temprature
    Temprature=float(Temprature)
    max_time=item_latest.max_time
    max_time=int(max_time)
    json_data = {
            "inference_service": Type_item,
            "messages": [
              {
                "role": "user",
                "content": query
              }
            ],
            "model": Model_item,
            "max_tokens": 4096,
            "stream": False,
            "temperature": Temprature,
            "timeout": max_time
    }
    print(json_data)
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