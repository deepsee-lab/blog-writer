from loguru import logger
from fastapi import APIRouter,UploadFile
from configs.config import ROOT_DIR
import aiofiles,os,requests
from apps.scripts import service
from pydantic import BaseModel, Field
import json
router = APIRouter(
    prefix="/api/v1"
)

class Response(BaseModel):
    code: str
    message: str
    data: dict

@router.get("/heartbeat")
def heartbeat():
    logger.info('run heartbeat')
    return 'heartbeat'

##############################################################################################
#  网页功能部分
##############################################################################################

########################
#  upload
#######################



@router.post('/upload/file' )
async def upload_qiniu(files: list[UploadFile]):
    upload_results = []

    for file in files:
        # 保存上传的文件
        upload_file_path = os.path.join(ROOT_DIR, file.filename)
        
        # 异步写入文件
        async with aiofiles.open(upload_file_path, "wb+") as out_file:
            while content := await file.read(1024):  # 分块读取文件并写入
                await out_file.write(content)
        
        url = 'http://127.0.0.1:6070/upload'
        bucket_name = os.getenv('BUCKET_NAME')
        upload_result = service.qiniu_upload(url, bucket_name, upload_file_path)

        if upload_result['success']:
            qiniu_url = upload_result['data']['url']
            upload_results.append({
                'filename': file.filename,
                'url': qiniu_url,
                'status': 'success'
            })
        else:
            upload_results.append({
                'filename': file.filename,
                'url': None,
                'status': 'failed'
            })

    if all(result['status'] == 'success' for result in upload_results):
        return {
            'message': '所有文件上传成功',
            'data': upload_results,
            'code': 200
        }
    else:
        return {
            'message': '部分或全部文件上传失败',
            'data': upload_results,
            'code': 500
        }

@router.post('/get/iamge_desc')
def iamge_desc(
    request_data: dict = {
    "images": [
        "http://smw76g823.hn-bkt.clouddn.com/jpg/bc0e427ef32e4c4ea63e3057a9cb621d.jpg", 
        "http://smw76g823.hn-bkt.clouddn.com/jpg/78caaac2161b47578602fced6409ff57.jpg"
        ],
    "style": "自然流畅",
    "language": "中文",
    "length": "200",
    "summary_length": "400",
    "temperature": 0.3,
    "type_name":'xinference',
    "model_select":"MiniCPM-V-2.6"
}
):
    # 校验 request_data 是否有效
    if not request_data or not isinstance(request_data, dict):
        return Response(
            code="400",
            message="Invalid request data. Must be a JSON object.",
            data={}
        )

    # 从 JSON 数据中提取参数
    try:
        images = request_data.get("images", [])
        type_name = request_data.get("type_name", "xinference")
        model_select = request_data.get("model_select", "MiniCPM-V-2.6-8B")
        style = request_data.get("style", "自然流畅")
        language = request_data.get("language", "中文")
        length = request_data.get("length", "200")
        summary_length = request_data.get("summary_length", "400")
        temperature = request_data.get("temperature", 0.8)
        url = request_data.get("url", "http://127.0.0.1:4010/private/inference")
    except Exception as e:
        return Response(
            code="400",
            message=f"Invalid request data: {str(e)}",
            data={}
        )

    # 参数校验
    if not isinstance(images, list) or not all(isinstance(img, str) for img in images):
        return Response(
            code="400",
            message="Invalid images format. Must be a list of strings.",
            data={}
        )

    print("Received images:", images)
    url="http://127.0.0.1:6050/travel/generate/image_group"
    result=service.get_image_group(url,images,type_name,model_select,style,language,length,summary_length,temperature)
    print(result)
    if result['code']=='000000':
        image_descriptions=result['data']
        return {
            'message':'success',
            'data':{
                'descriptions':image_descriptions},
            'code':result['code']
        }
    else:
         return {
            'message':'fail',
            'data':{
                },
            'code':result['code']
        }

@router.post('/get/frame')
def get_frame(request_data: dict = {
    "image_desc": {
        "status":True,
        "data": {
               "descriptions": {
                 "http://smw76g823.hn-bkt.clouddn.com/jpg/bc0e427ef32e4c4ea63e3057a9cb621d.jpg": "这幅图片展示了一座在黄昏时分的现代化斜拉桥的全景视图。天空呈现出从温暖的橙色到深蓝色的渐变色调，暗示着日落时刻。桥梁被点亮，与暮色形成鲜明对比，并反射在下面宁静的水面上，营造出一种镜像效果。桥塔高耸，缆绳将重量分配到支撑结构上。在远处，可以看到一个城市天际线，建筑物点缀着灯光，显示了人类居住和活动的存在。车辆的车灯形成了运动模糊的光轨，表明照片拍摄时车辆在移动。整体氛围宁静而美丽，展示了工程壮举与自然之美之间的和谐融合。",
                 "http://smw76g823.hn-bkt.clouddn.com/jpg/78caaac2161b47578602fced6409ff57.jpg": "这幅图片展示了一个结合了城市和自然元素的全景景观。在前景，有一条弯曲的道路穿过郁郁葱葱的绿地，几辆汽车在路上行驶，显示出轻度交通流量。道路两侧是高大的树木和灌木，表明这是一个维护良好的公园或林区。中景展示了密集的住宅建筑群，包括多层公寓楼和一些独立的建筑物。这些结构以白色、米色和灰色为主色调，带有红色屋顶，与周围绿植形成对比。背景逐渐过渡到一个更开阔的城市天际线，可见更多高层建筑，天空呈现出淡蓝色，并有粉色云彩的迹象，可能表明这是黎明或黄昏时分。整个场景传达出一种宁静的城市生活感觉，自然环境与城市发展和谐共存。"
               },
               "unified_text": "这幅图片展示了一座在黄昏时分的现代化斜拉桥的全景视图。天空呈现出从温暖的橙色到深蓝色的渐变色调，暗示着日落时刻。桥梁被点亮，与暮色形成鲜明对比，并反射在下面宁静的水面上，营造出一种镜像效果。桥塔高耸，缆绳将重量分配到支撑结构上。在远处，可以看到一个城市天际线，建筑物点缀着灯光，显示了人类居住和活动的存在。车辆的车灯形成了运动模糊的光轨，表明照片拍摄时车辆在移动。整体氛围宁静而美丽，展示了工程壮举与自然之美之间的和谐融合。\n\n这幅图片展示了一个结合了城市和自然元素的全景景观。在前景，有一条弯曲的道路穿过郁郁葱葱的绿地，几辆汽车在路上行驶，显示出轻度交通流量。道路两侧是高大的树木和灌木，表明这是一个维护良好的公园或林区。中景展示了密集的住宅建筑群，包括多层公寓楼和一些独立的建筑物。这些结构以白色、米色和灰色为主色调，带有红色屋顶，与周围绿植形成对比。背景逐渐过渡到一个更开阔的城市天际线，可见更多高层建筑，天空呈现出淡蓝色，并有粉色云彩的迹象，可能表明这是黎明或黄昏时分。整个场景传达出一种宁静的城市生活感觉，自然环境与城市发展和谐共存。\n\n这幅图片捕捉到了现代都市生活中宁静的一面。黄昏时分的桥梁，不仅是一座连接城市的纽带，也是一道美丽的风景线。它映射出人类智慧与自然和谐共处的美好愿景。在这片宁静中，我们可以感受到城市的脉动，也能找到内心的平静。这样的景象，不仅让我们欣赏到现代建筑的雄伟，更让我们思考人与自然的关系，如何在发展中保护环境，实现可持续发展。总的来说，这幅图片是一幅美丽而富有启示性的作品，值得我们细细品味和反思。"
             }
    },
    "travel_descriptions":"今日武汉夜游，很开心",
    "theme": "武汉之旅",
    "temperature": 0.3,
    "type_name":'xinference',
    "model_select":"MiniCPM-V-2.6-8B"
}
):
    # 校验 request_data 是否有效
    if not request_data or not isinstance(request_data, dict):
        return Response(
            code="400",
            message="Invalid request data. Must be a JSON object.",
            data={}
        )

    # 从 JSON 数据中提取参数
    try:
        theme = request_data.get("theme")
        image_descriptions = request_data.get("image_desc", {})
        type_name = request_data.get("type_name", "xinference")
        model_select = request_data.get("model_select", "MiniCPM-V-2.6-8B")
        temperature = request_data.get("temperature", 0.8)
        travel_descriptions = request_data.get("travel_descriptions", '今日武汉夜游，很开心')
    except Exception as e:
        return Response(
            code="400",
            message=f"Invalid request data: {str(e)}",
            data={}
        )
    # 参数校验
    if not theme or not isinstance(theme, str):
        return Response(
            code="400",
            message="Invalid theme. Must be a non-empty string.",
            data={}
        )

    # 调用内部逻辑
    try:
        url="http://127.0.0.1:6050/travel/generate/frame_work"
        result = service.frame_work(
            url, theme, image_descriptions,type_name,model_select,temperature,travel_descriptions
        )
        print("travel_generate result:", result)
        print(result['code'])
        print(type(result['data']['content']))
        try:
            json_data=json.loads(result['data']['content'])
            print('1111')
            print(type(json_data))
        except:
            json_data=result['data']['content']
        
        result['data']['content']=json_data
        if result['code']=='000000':  # 如果 status 为 True
            return Response(
                code="000000",
                message=result.get('message', "Success"),
                data=result.get('data', {})
            )
        else:
            return Response(
                code="404",
                message=result.get('message', "Processing failed"),
                data={}
            )
    except Exception as e:
        print("Error in processing:", e)
        return Response(
            code="500",
            message=f"Internal server error: {str(e)}",
            data={}
        )

@router.post('/get/result')
def get_result(request_data: dict = 
                      {
                            "theme":'武汉之旅',
                            "outline":"# 武汉之旅\n\n## 一、前言\n\n在繁忙的城市生活中，我们偶尔需要一个放松的假期来充电。这次我选择了武汉，这座拥有悠久历史和丰富文化底蕴的城市，开启了一场充满惊喜的旅程。\n\n## 二、武汉的历史与文化\n\n武汉，古称江夏，是中国历史文化名城之一。在这里，我参观了黄鹤楼，这座著名的古建筑见证了武汉的千年变迁。漫步在长江大桥上，我感受到了这座城市的雄伟气魄。\n\n## 三、美食之旅\n\n武汉的美食是这座城市的另一张名片。我品尝了热干面、鸭脖、糯米鸡等特色小吃，每一道美食都让我回味无穷。尤其是武昌鱼，鲜嫩可口，让人垂涎欲滴。\n\n## 四、自然风光\n\n除了城市风光，武汉还有许多美丽的自然景观。东湖绿道是我此次旅行中最难忘的地方之一。在这里，我骑着自行车，沿着湖边的小路，享受着清新的空气和宜人的景色。\n\n## 五、购物体验\n\n在武汉，我不仅品味了美食，还购买了许多具有地方特色的纪念品。在汉街的商场里，我买到了精美的瓷器和丝绸制品，这些都是武汉文化的代表。\n\n## 六、结语\n\n此次武汉之旅，让我领略了这座城市的独特魅力。无论是历史遗迹、美食美景还是购物体验，都给我留下了深刻的印象。我相信，未来我还会再次踏上这片土地，继续探索它的无限可能。\n\n在这次武汉之旅中，我不仅放松了身心，还增进了对这座城市的认识。希望我的游记能为你的武汉之行提供一些参考，期待与你在武汉的下一次相遇。",
                            "image_descriptions": {
                                "status":True,
                                "data": {
                                       "descriptions": {
                                         "http://smw76g823.hn-bkt.clouddn.com/jpg/bc0e427ef32e4c4ea63e3057a9cb621d.jpg": "这幅图片展示了一座在黄昏时分的现代化斜拉桥的全景视图。天空呈现出从温暖的橙色到深蓝色的渐变色调，暗示着日落时刻。桥梁被点亮，与暮色形成鲜明对比，并反射在下面宁静的水面上，营造出一种镜像效果。桥塔高耸，缆绳将重量分配到支撑结构上。在远处，可以看到一个城市天际线，建筑物点缀着灯光，显示了人类居住和活动的存在。车辆的车灯形成了运动模糊的光轨，表明照片拍摄时车辆在移动。整体氛围宁静而美丽，展示了工程壮举与自然之美之间的和谐融合。",
                                         "http://smw76g823.hn-bkt.clouddn.com/jpg/78caaac2161b47578602fced6409ff57.jpg": "这幅图片展示了一个结合了城市和自然元素的全景景观。在前景，有一条弯曲的道路穿过郁郁葱葱的绿地，几辆汽车在路上行驶，显示出轻度交通流量。道路两侧是高大的树木和灌木，表明这是一个维护良好的公园或林区。中景展示了密集的住宅建筑群，包括多层公寓楼和一些独立的建筑物。这些结构以白色、米色和灰色为主色调，带有红色屋顶，与周围绿植形成对比。背景逐渐过渡到一个更开阔的城市天际线，可见更多高层建筑，天空呈现出淡蓝色，并有粉色云彩的迹象，可能表明这是黎明或黄昏时分。整个场景传达出一种宁静的城市生活感觉，自然环境与城市发展和谐共存。"
                                       },
                                       "unified_text": "这幅图片展示了一座在黄昏时分的现代化斜拉桥的全景视图。天空呈现出从温暖的橙色到深蓝色的渐变色调，暗示着日落时刻。桥梁被点亮，与暮色形成鲜明对比，并反射在下面宁静的水面上，营造出一种镜像效果。桥塔高耸，缆绳将重量分配到支撑结构上。在远处，可以看到一个城市天际线，建筑物点缀着灯光，显示了人类居住和活动的存在。车辆的车灯形成了运动模糊的光轨，表明照片拍摄时车辆在移动。整体氛围宁静而美丽，展示了工程壮举与自然之美之间的和谐融合。\n\n这幅图片展示了一个结合了城市和自然元素的全景景观。在前景，有一条弯曲的道路穿过郁郁葱葱的绿地，几辆汽车在路上行驶，显示出轻度交通流量。道路两侧是高大的树木和灌木，表明这是一个维护良好的公园或林区。中景展示了密集的住宅建筑群，包括多层公寓楼和一些独立的建筑物。这些结构以白色、米色和灰色为主色调，带有红色屋顶，与周围绿植形成对比。背景逐渐过渡到一个更开阔的城市天际线，可见更多高层建筑，天空呈现出淡蓝色，并有粉色云彩的迹象，可能表明这是黎明或黄昏时分。整个场景传达出一种宁静的城市生活感觉，自然环境与城市发展和谐共存。\n\n这幅图片捕捉到了现代都市生活中宁静的一面。黄昏时分的桥梁，不仅是一座连接城市的纽带，也是一道美丽的风景线。它映射出人类智慧与自然和谐共处的美好愿景。在这片宁静中，我们可以感受到城市的脉动，也能找到内心的平静。这样的景象，不仅让我们欣赏到现代建筑的雄伟，更让我们思考人与自然的关系，如何在发展中保护环境，实现可持续发展。总的来说，这幅图片是一幅美丽而富有启示性的作品，值得我们细细品味和反思。"
                                     }
                            },
                            "temperature": 0.3,
                            "type_name":'xinference',
                            "model_select":"MiniCPM-V-2.6-8B"
                        }):
    # 校验 request_data 是否有效
    if not request_data or not isinstance(request_data, dict):
        return Response(
            code="400",
            message="Invalid request data. Must be a JSON object.",
            data={}
        )

    # 从 JSON 数据中提取参数
    try:
        theme = request_data.get("theme")
        outline = request_data.get("outline")
        print('aaa:',outline)
        image_descriptions = request_data.get("image_descriptions", {})
        type_name = request_data.get("type_name", "xinference")
        model_select = request_data.get("model_select", "MiniCPM-V-2.6-8B")
        url = request_data.get("url", "http://127.0.0.1:4010/private/inference")
        temperature = request_data.get("temperature", 0.8)
    except Exception as e:
        return Response(
            code="400",
            message=f"Invalid request data: {str(e)}",
            data={}
        )

    # 参数校验
    if not theme or not isinstance(theme, str):
        return Response(
            code="400",
            message="Invalid theme. Must be a non-empty string.",
            data={}
        )

    if not outline or not isinstance(outline, str):
        return Response(
            code="400",
            message="Invalid outline. Must be a non-empty string.",
            data={}
        )
    url="http://127.0.0.1:6050/travel/generate/travel_result"
    result=service.travel_result(url,theme, outline, image_descriptions,type_name,model_select,temperature)
    if result['code']=='000000':
        content=result['data']
        return {
            'success':True,
            'data':content,
            'code':result['code']
        }
    else:
        return {
            'success':False,
            'message': result,
            'code':result['code']
        }

@router.post('/get/markdown')
def get_result(request_data: dict = 
                      {
                            "data":{
                                    "title": "武汉之旅",
                                    "outline": "# 武汉之旅\n\n## 一、前言\n\n在繁忙的城市生活中，我们偶尔需要一个放松的假期来充电。这次我选择了武汉，这座拥有悠久历史和丰富文化底蕴的城市，开启了一场充满惊喜的旅程。\n\n## 二、武汉的历史与文化\n\n武汉，古称江夏，是中国历史文化名城之一。在这里，我参观了黄鹤楼，这座著名的古建筑见证了武汉的千年变迁。漫步在长江大桥上，我感受到了这座城市的雄伟气魄。\n\n## 三、美食之旅\n\n武汉的美食是这座城市的另一张名片。我品尝了热干面、鸭脖、糯米鸡等特色小吃，每一道美食都让我回味无穷。尤其是武昌鱼，鲜嫩可口，让人垂涎欲滴。\n\n## 四、自然风光\n\n除了城市风光，武汉还有许多美丽的自然景观。东湖绿道是我此次旅行中最难忘的地方之一。在这里，我骑着自行车，沿着湖边的小路，享受着清新的空气和宜人的景色。\n\n## 五、购物体验\n\n在武汉，我不仅品味了美食，还购买了许多具有地方特色的纪念品。在汉街的商场里，我买到了精美的瓷器和丝绸制品，这些都是武汉文化的代表。\n\n## 六、结语\n\n此次武汉之旅，让我领略了这座城市的独特魅力。无论是历史遗迹、美食美景还是购物体验，都给我留下了深刻的印象。我相信，未来我还会再次踏上这片土地，继续探索它的无限可能。\n\n在这次武汉之旅中，我不仅放松了身心，还增进了对这座城市的认识。希望我的游记能为你的武汉之行提供一些参考，期待与你在武汉的下一次相遇。",
                                    "content": "武汉之旅\n\n引言：\n在这个繁忙的城市生活中，我们总需要寻找一片宁静之地来放松身心，充电再出发。这次，我选择了武汉作为我的目的地，开启了一场充满惊喜的旅程。\n\n第一站：历史与文化\n\n武汉，古称江夏，是中华文明的重要发源地之一。在这次旅行中，我参观了黄鹤楼，这座有着千年历史的古建筑见证了武汉的变迁与发展。漫步在黄鹤楼上，我仿佛穿越时空，感受到了千年前的繁华与辉煌。站在长江大桥上，我眺望着滚滚江水，感叹着这座城市的雄伟气魄。\n\n第二站：美食之旅\n\n武汉不仅拥有悠久的历史，还有丰富的美食文化。在这里，我品尝了热干面、鸭脖和糯米鸡等特色小吃。其中，汉街的美食更是让我流连忘返。无论是精致的瓷器还是精美的丝绸制品，都让我对武汉的文化底蕴有了更深的理解。\n\n第三站：自然风光\n\n除了历史和美食，武汉的自然风光也令人叹为观止。东湖绿道是我此次旅行中最难忘的地方。骑行在绿道上，四周绿树成荫，湖水清澈见底，让人感受到大自然的美好。这里的美景让我暂时忘却了城市的喧嚣，享受着片刻的宁静与惬意。\n\n第四站：购物体验\n\n在武汉的购物体验也是一大亮点。我在汉街的商场里购买了许多具有武汉特色的纪念品，如精美的瓷器和丝绸制品。这些独特的商品不仅让我带回家留作纪念，还让我更加了解了这座城市的文化内涵。\n\n第五站：总结与期望\n\n这次武汉之旅让我收获颇丰，不仅领略了这座城市的独特魅力，还增进了对中华文化的认识。武汉的历史、美食、自然风光以及购物体验都给我留下了深刻的印象。期待下次再来武汉，继续探索这个充满活力与文化底蕴的城市。\n\n结语：\n\n武汉之旅不仅仅是一次旅行，更是一段心灵的洗礼。在这里，我感受到了这座城市的脉搏，体会到了生活的美好。希望每个人都能有机会来到武汉，体验这座城市的独特魅力。",
                                    "images": {
                                      "network": [
                                        "http://smw76g823.hn-bkt.clouddn.com/jpg/bc0e427ef32e4c4ea63e3057a9cb621d.jpg",
                                        "http://smw76g823.hn-bkt.clouddn.com/jpg/78caaac2161b47578602fced6409ff57.jpg"
                                      ],
                                      "local": []
                                    },
                                    "unified_text": "",
                                    "descriptions": [
                                      {
                                        "path": "http://smw76g823.hn-bkt.clouddn.com/jpg/bc0e427ef32e4c4ea63e3057a9cb621d.jpg",
                                        "description": "这幅图片展示了一座在黄昏时分的现代化斜拉桥的全景视图。天空呈现出从温暖的橙色到深蓝色的渐变色调，暗示着日落时刻。桥梁被点亮，与暮色形成鲜明对比，并反射在下面宁静的水面上，营造出一种镜像效果。桥塔高耸，缆绳将重量分配到支撑结构上。在远处，可以看到一个城市天际线，建筑物点缀着灯光，显示了人类居住和活动的存在。车辆的车灯形成了运动模糊的光轨，表明照片拍摄时车辆在移动。整体氛围宁静而美丽，展示了工程壮举与自然之美之间的和谐融合。",
                                        "is_url": True
                                      },
                                      {
                                        "path": "http://smw76g823.hn-bkt.clouddn.com/jpg/78caaac2161b47578602fced6409ff57.jpg",
                                        "description": "这幅图片展示了一个结合了城市和自然元素的全景景观。在前景，有一条弯曲的道路穿过郁郁葱葱的绿地，几辆汽车在路上行驶，显示出轻度交通流量。道路两侧是高大的树木和灌木，表明这是一个维护良好的公园或林区。中景展示了密集的住宅建筑群，包括多层公寓楼和一些独立的建筑物。这些结构以白色、米色和灰色为主色调，带有红色屋顶，与周围绿植形成对比。背景逐渐过渡到一个更开阔的城市天际线，可见更多高层建筑，天空呈现出淡蓝色，并有粉色云彩的迹象，可能表明这是黎明或黄昏时分。整个场景传达出一种宁静的城市生活感觉，自然环境与城市发展和谐共存。",
                                        "is_url": True
                                      }
                                    ]
                                  },
                            "img_width":600,
                            "temperature": 0.3,
                            "type_name":'xinference',
                            "model_select":"MiniCPM-V-2.6-8B"
                        }):
    # 校验 request_data 是否有效
    if not request_data or not isinstance(request_data, dict):
        return Response(
            code="400",
            message="Invalid request data. Must be a JSON object.",
            data={}
        )

    # 从 JSON 数据中提取参数
    try:
        data = request_data.get("data")
        img_width = request_data.get("img_width")
        type_name = request_data.get("type_name", "xinference")
        model_select = request_data.get("model_select", "MiniCPM-V-2.6-8B")
        temperature = request_data.get("temperature", 0.8)
    except Exception as e:
        return Response(
            code="400",
            message=f"Invalid request data: {str(e)}",
            data={}
        )

    url="http://127.0.0.1:6050/travel/generate/mark_down"
    result=service.post_server(url,data={
        "data":data,
        "img_width":img_width,
        "type_name":type_name,
        "model_select":model_select,
        "temperature":temperature
    })
    if result['code']=='000000':
        content=result['data']
        return {
            'message':'success',
            'data':content,
            'code':result['code']
        }
    else:
        return {
            'data':{},
            'message': result,
            'code':result['code']
        }

@router.post('/get/frame_xiaohongshu')
def get_frame_xiaohongshu(request_data: dict = {
    "image_desc": {
        "status":True,
        "data": {
               "descriptions": {
                 "http://smw76g823.hn-bkt.clouddn.com/jpg/bc0e427ef32e4c4ea63e3057a9cb621d.jpg": "这幅图片展示了一座在黄昏时分的现代化斜拉桥的全景视图。天空呈现出从温暖的橙色到深蓝色的渐变色调，暗示着日落时刻。桥梁被点亮，与暮色形成鲜明对比，并反射在下面宁静的水面上，营造出一种镜像效果。桥塔高耸，缆绳将重量分配到支撑结构上。在远处，可以看到一个城市天际线，建筑物点缀着灯光，显示了人类居住和活动的存在。车辆的车灯形成了运动模糊的光轨，表明照片拍摄时车辆在移动。整体氛围宁静而美丽，展示了工程壮举与自然之美之间的和谐融合。",
                 "http://smw76g823.hn-bkt.clouddn.com/jpg/78caaac2161b47578602fced6409ff57.jpg": "这幅图片展示了一个结合了城市和自然元素的全景景观。在前景，有一条弯曲的道路穿过郁郁葱葱的绿地，几辆汽车在路上行驶，显示出轻度交通流量。道路两侧是高大的树木和灌木，表明这是一个维护良好的公园或林区。中景展示了密集的住宅建筑群，包括多层公寓楼和一些独立的建筑物。这些结构以白色、米色和灰色为主色调，带有红色屋顶，与周围绿植形成对比。背景逐渐过渡到一个更开阔的城市天际线，可见更多高层建筑，天空呈现出淡蓝色，并有粉色云彩的迹象，可能表明这是黎明或黄昏时分。整个场景传达出一种宁静的城市生活感觉，自然环境与城市发展和谐共存。"
               },
               "unified_text": "这幅图片展示了一座在黄昏时分的现代化斜拉桥的全景视图。天空呈现出从温暖的橙色到深蓝色的渐变色调，暗示着日落时刻。桥梁被点亮，与暮色形成鲜明对比，并反射在下面宁静的水面上，营造出一种镜像效果。桥塔高耸，缆绳将重量分配到支撑结构上。在远处，可以看到一个城市天际线，建筑物点缀着灯光，显示了人类居住和活动的存在。车辆的车灯形成了运动模糊的光轨，表明照片拍摄时车辆在移动。整体氛围宁静而美丽，展示了工程壮举与自然之美之间的和谐融合。\n\n这幅图片展示了一个结合了城市和自然元素的全景景观。在前景，有一条弯曲的道路穿过郁郁葱葱的绿地，几辆汽车在路上行驶，显示出轻度交通流量。道路两侧是高大的树木和灌木，表明这是一个维护良好的公园或林区。中景展示了密集的住宅建筑群，包括多层公寓楼和一些独立的建筑物。这些结构以白色、米色和灰色为主色调，带有红色屋顶，与周围绿植形成对比。背景逐渐过渡到一个更开阔的城市天际线，可见更多高层建筑，天空呈现出淡蓝色，并有粉色云彩的迹象，可能表明这是黎明或黄昏时分。整个场景传达出一种宁静的城市生活感觉，自然环境与城市发展和谐共存。\n\n这幅图片捕捉到了现代都市生活中宁静的一面。黄昏时分的桥梁，不仅是一座连接城市的纽带，也是一道美丽的风景线。它映射出人类智慧与自然和谐共处的美好愿景。在这片宁静中，我们可以感受到城市的脉动，也能找到内心的平静。这样的景象，不仅让我们欣赏到现代建筑的雄伟，更让我们思考人与自然的关系，如何在发展中保护环境，实现可持续发展。总的来说，这幅图片是一幅美丽而富有启示性的作品，值得我们细细品味和反思。"
             }
    },
    "theme": "武汉之旅",
    "temperature": 0.3,
    "type_name":'xinference',
    "model_select":"MiniCPM-V-2.6-8B"
}
):
    # 校验 request_data 是否有效
    if not request_data or not isinstance(request_data, dict):
        return Response(
            code="400",
            message="Invalid request data. Must be a JSON object.",
            data={}
        )

    # 从 JSON 数据中提取参数
    try:
        theme = request_data.get("theme")
        image_descriptions = request_data.get("image_desc", {})
        type_name = request_data.get("type_name", "xinference")
        model_select = request_data.get("model_select", "MiniCPM-V-2.6-8B")
        temperature = request_data.get("temperature", 0.8)
    except Exception as e:
        return Response(
            code="400",
            message=f"Invalid request data: {str(e)}",
            data={}
        )
    print('13579:',theme)
    # 参数校验
    if not theme or not isinstance(theme, str):
        return Response(
            code="400",
            message="Invalid theme. Must be a non-empty string.",
            data={}
        )

    # 调用内部逻辑
    try:
        url="http://127.0.0.1:6050/travel/generate/frame_work_xiaohongshu"
        result = service.post_server(url,data = {
        "theme": theme,
        "image_desc": image_descriptions,
        "type_name":type_name,
        "model_select":model_select,
        "temperature":temperature
    })
        print("travel_generate result:", result)
        print(result['code'])
        if result['code']=='000000':  # 如果 status 为 True
            return Response(
                code="000000",
                message=result.get('message', "Success"),
                data=result.get('data', {})
            )
        else:
            return Response(
                code="404",
                message=result.get('message', "Processing failed"),
                data={}
            )
    except Exception as e:
        print("Error in processing:", e)
        return Response(
            code="500",
            message=f"Internal server error: {str(e)}",
            data={}
        )

@router.post('/get/models' )
async def model_list(inference_service:str='xinference'):
    url='http://127.0.0.1:4010/private/models'
    result=service.post_server(url,data={
        "inference_service":inference_service
    })
    if result['code']=='000000':  # 如果 status 为 True
            return Response(
                code="000000",
                message=result.get('message', "Success"),
                data=result.get('data', {})
            )
    else:
            return Response(
                code="404",
                message=result.get('message', "Processing failed"),
                data={}
            )

@router.post('/get/markdown2json')
def get_result_json(request_data: dict = 
                      {
                            "data":{
                                    "title": "武汉之旅",
                                    "outline": "# 武汉之旅\n\n## 一、前言\n\n在繁忙的城市生活中，我们偶尔需要一个放松的假期来充电。这次我选择了武汉，这座拥有悠久历史和丰富文化底蕴的城市，开启了一场充满惊喜的旅程。\n\n## 二、武汉的历史与文化\n\n武汉，古称江夏，是中国历史文化名城之一。在这里，我参观了黄鹤楼，这座著名的古建筑见证了武汉的千年变迁。漫步在长江大桥上，我感受到了这座城市的雄伟气魄。\n\n## 三、美食之旅\n\n武汉的美食是这座城市的另一张名片。我品尝了热干面、鸭脖、糯米鸡等特色小吃，每一道美食都让我回味无穷。尤其是武昌鱼，鲜嫩可口，让人垂涎欲滴。\n\n## 四、自然风光\n\n除了城市风光，武汉还有许多美丽的自然景观。东湖绿道是我此次旅行中最难忘的地方之一。在这里，我骑着自行车，沿着湖边的小路，享受着清新的空气和宜人的景色。\n\n## 五、购物体验\n\n在武汉，我不仅品味了美食，还购买了许多具有地方特色的纪念品。在汉街的商场里，我买到了精美的瓷器和丝绸制品，这些都是武汉文化的代表。\n\n## 六、结语\n\n此次武汉之旅，让我领略了这座城市的独特魅力。无论是历史遗迹、美食美景还是购物体验，都给我留下了深刻的印象。我相信，未来我还会再次踏上这片土地，继续探索它的无限可能。\n\n在这次武汉之旅中，我不仅放松了身心，还增进了对这座城市的认识。希望我的游记能为你的武汉之行提供一些参考，期待与你在武汉的下一次相遇。",
                                    "content": "武汉之旅\n\n引言：\n在这个繁忙的城市生活中，我们总需要寻找一片宁静之地来放松身心，充电再出发。这次，我选择了武汉作为我的目的地，开启了一场充满惊喜的旅程。\n\n第一站：历史与文化\n\n武汉，古称江夏，是中华文明的重要发源地之一。在这次旅行中，我参观了黄鹤楼，这座有着千年历史的古建筑见证了武汉的变迁与发展。漫步在黄鹤楼上，我仿佛穿越时空，感受到了千年前的繁华与辉煌。站在长江大桥上，我眺望着滚滚江水，感叹着这座城市的雄伟气魄。\n\n第二站：美食之旅\n\n武汉不仅拥有悠久的历史，还有丰富的美食文化。在这里，我品尝了热干面、鸭脖和糯米鸡等特色小吃。其中，汉街的美食更是让我流连忘返。无论是精致的瓷器还是精美的丝绸制品，都让我对武汉的文化底蕴有了更深的理解。\n\n第三站：自然风光\n\n除了历史和美食，武汉的自然风光也令人叹为观止。东湖绿道是我此次旅行中最难忘的地方。骑行在绿道上，四周绿树成荫，湖水清澈见底，让人感受到大自然的美好。这里的美景让我暂时忘却了城市的喧嚣，享受着片刻的宁静与惬意。\n\n第四站：购物体验\n\n在武汉的购物体验也是一大亮点。我在汉街的商场里购买了许多具有武汉特色的纪念品，如精美的瓷器和丝绸制品。这些独特的商品不仅让我带回家留作纪念，还让我更加了解了这座城市的文化内涵。\n\n第五站：总结与期望\n\n这次武汉之旅让我收获颇丰，不仅领略了这座城市的独特魅力，还增进了对中华文化的认识。武汉的历史、美食、自然风光以及购物体验都给我留下了深刻的印象。期待下次再来武汉，继续探索这个充满活力与文化底蕴的城市。\n\n结语：\n\n武汉之旅不仅仅是一次旅行，更是一段心灵的洗礼。在这里，我感受到了这座城市的脉搏，体会到了生活的美好。希望每个人都能有机会来到武汉，体验这座城市的独特魅力。",
                                    "images": {
                                      "network": [
                                        "http://smw76g823.hn-bkt.clouddn.com/jpg/bc0e427ef32e4c4ea63e3057a9cb621d.jpg",
                                        "http://smw76g823.hn-bkt.clouddn.com/jpg/78caaac2161b47578602fced6409ff57.jpg"
                                      ],
                                      "local": []
                                    },
                                    "unified_text": "",
                                    "descriptions": [
                                      {
                                        "path": "http://smw76g823.hn-bkt.clouddn.com/jpg/bc0e427ef32e4c4ea63e3057a9cb621d.jpg",
                                        "description": "这幅图片展示了一座在黄昏时分的现代化斜拉桥的全景视图。天空呈现出从温暖的橙色到深蓝色的渐变色调，暗示着日落时刻。桥梁被点亮，与暮色形成鲜明对比，并反射在下面宁静的水面上，营造出一种镜像效果。桥塔高耸，缆绳将重量分配到支撑结构上。在远处，可以看到一个城市天际线，建筑物点缀着灯光，显示了人类居住和活动的存在。车辆的车灯形成了运动模糊的光轨，表明照片拍摄时车辆在移动。整体氛围宁静而美丽，展示了工程壮举与自然之美之间的和谐融合。",
                                        "is_url": True
                                      },
                                      {
                                        "path": "http://smw76g823.hn-bkt.clouddn.com/jpg/78caaac2161b47578602fced6409ff57.jpg",
                                        "description": "这幅图片展示了一个结合了城市和自然元素的全景景观。在前景，有一条弯曲的道路穿过郁郁葱葱的绿地，几辆汽车在路上行驶，显示出轻度交通流量。道路两侧是高大的树木和灌木，表明这是一个维护良好的公园或林区。中景展示了密集的住宅建筑群，包括多层公寓楼和一些独立的建筑物。这些结构以白色、米色和灰色为主色调，带有红色屋顶，与周围绿植形成对比。背景逐渐过渡到一个更开阔的城市天际线，可见更多高层建筑，天空呈现出淡蓝色，并有粉色云彩的迹象，可能表明这是黎明或黄昏时分。整个场景传达出一种宁静的城市生活感觉，自然环境与城市发展和谐共存。",
                                        "is_url": True
                                      }
                                    ]
                                  },
                            "img_width":600,
                            "temperature": 0.3,
                            "type_name":'xinference',
                            "model_select":"MiniCPM-V-2.6-8B"
                        }):
    # 校验 request_data 是否有效
    if not request_data or not isinstance(request_data, dict):
        return Response(
            code="400",
            message="Invalid request data. Must be a JSON object.",
            data={}
        )

    # 从 JSON 数据中提取参数
    try:
        data = request_data.get("data")
        img_width = request_data.get("img_width")
        type_name = request_data.get("type_name", "xinference")
        model_select = request_data.get("model_select", "MiniCPM-V-2.6-8B")
        temperature = request_data.get("temperature", 0.8)
    except Exception as e:
        return Response(
            code="400",
            message=f"Invalid request data: {str(e)}",
            data={}
        )

    url="http://127.0.0.1:6050/travel/generate/mark_down"
    result=service.post_server(url,data={
        "data":data,
        "img_width":img_width,
        "type_name":type_name,
        "model_select":model_select,
        "temperature":temperature
    })
    if result['code']=='000000':
        content=result['data']
        url="http://127.0.0.1:6050/travel/generate/md2json"
        result=service.post_server(url,data={
            "markdown_file":content['markdown_content'],
            "type_name":type_name,
            "model_select":model_select,
            "temperature":temperature
        })
        if result['code']=='000000':
            return {
                'message':'sucess',
                'data':result['data'],
                'code':result['code']
            }
    else:
        return {
            'data':{},
            'message': result,
            'code':result['code']
        }