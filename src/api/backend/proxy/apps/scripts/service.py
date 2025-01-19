import requests
from loguru import logger


def qiniu_upload(url,bucket_name,localfile):
    #url = 'http://127.0.0.1:6070/upload'
    logger.info('qiniu:')
    print(bucket_name,localfile)
    json_data = {
        "bucket_name": bucket_name,
        "localfile": localfile,
    }
    # 发送请求并存储响应
    response = requests.post(url, json=json_data).json()
    return response

def get_image_group(url, images,type_name,model_select, style="自然流畅", language="中文", length="200", summary_length="400", temperature=0.8):
    print('get_image_group:', images, url)
    data = {
        "images": images,  # 将图片列表作为查询参数
        "type_name":type_name,
        "model_select":model_select,
        "style": style,
        "language": language,
        "length": length,
        "summary_length": summary_length,
        "temperature": temperature
    }
    response = requests.post(url, json=data)
    try:
        response_data = response.json()
        print("Response JSON1:", response_data)
        print("Response JSON1 type:", type(response_data))
        return response_data
    except Exception as e:
        print("Failed to parse response JSON1:", e)
        return {"code": 404, "message": str(e),'data':{}}


def frame_work(url, theme, image_desc,type_name,model_select,temperature,travel_descriptions):
    logger.info('frame_work:')
    print('image_desc123:', image_desc)

    data = {
        "theme": theme,
        "image_desc": image_desc,
        "type_name":type_name,
        "model_select":model_select,
        "temperature":temperature,
        "travel_descriptions":travel_descriptions
    }
    print("data:", data)

    response = requests.post(url, json=data)
    try:
        response_data = response.json()
        print("Response JSON1:", response_data)
        print("Response JSON1 type:", type(response_data))
        return response_data
    except Exception as e:
        print("Failed to parse response JSON1:", e)
        return {"code": 404, "message": str(e),'data':{}}

def travel_result(url,theme,outline,image_descriptions,type_name,model_select,temperature):
    #url = 'http://127.0.0.1:4010/generate/travel_result'
    logger.info('travel_result:')
    data = {
        "theme": theme,
        "outline": outline,
        "image_descriptions":image_descriptions,
        "type_name":type_name,
        "model_select":model_select,
        "temperature":temperature
    }
    # 发送请求并存储响应
    response = requests.post(url, json=data)
    try:
        response_data = response.json()
        print("Response JSON1:", response_data)
        print("Response JSON1 type:", type(response_data))
        return response_data
    except Exception as e:
        print("Failed to parse response JSON1:", e)
        return {"code": 404, "message": str(e),'data':{}}

def post_server(url,data):
    data 
    # 发送请求并存储响应
    response = requests.post(url, json=data)
    try:
        response_data = response.json()
        print("Response JSON1:", response_data)
        print("Response JSON1 type:", type(response_data))
        return response_data
    except Exception as e:
        print("Failed to parse response JSON1:", e)
        return {"code": 404, "message": str(e),'data':{}}

if __name__ == '__main__':
    url = 'http://127.0.0.1:4010/private/inference'
    KB_id="uuid0000000000000000000000000111"
    top_K=5
    query="种子"
    type_name='ollama'
    model_select='qwen2:1.5b-instruct-fp16'
    #answer=vector_model_rag(url,KB_id,top_K,query,type_name,model_select)
    #logger.info(answer)