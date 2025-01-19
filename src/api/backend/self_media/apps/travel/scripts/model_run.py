from loguru import logger
import requests,json

def model_rag(url,messages,type_name,model_select,temperature=0.7,timeout=6000,max_tokens=4096):
    #url = 'http://127.0.0.1:4010/private/inference'
    logger.info('model_run:')
    headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json'
    }
    json_data = {
        "messages": messages,
        "inference_service": type_name,
        "model": model_select,
        "max_tokens": max_tokens,
        "stream": False,
        "temperature": temperature,
        "timeout": timeout
    }
    json_string = json.dumps(json_data, indent=4)
    print('llll::',json_string)
    # 发送请求并存储响应
    try:
        response = requests.post(url, headers=headers,data=json_string)
        response = response.json()
        data=response['data']['result']['content']
        return {
            'code':200,
            'data':data,
            'message': '运行模型成功'
        }
    except Exception as e:
        return {
            'code':500,
            'data':{},
            'message':f'运行模型报错：{e}'
        }


    