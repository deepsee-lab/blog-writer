from loguru import logger
from fastapi import APIRouter
from typing import Optional
from pydantic import BaseModel, Field
from apps.travel.scripts import travel_generate as travel_generate

from typing import List
import json,re
router = APIRouter(
    prefix="/travel"
)


class DraftAddItem(BaseModel):
    access_token: str
    title: str = Field(default="title")
    author: Optional[str] = Field(default=None)
    digest: Optional[str] = Field(default=None)
    content: str = Field(default="content")
    content_source_url: Optional[str] = Field(default=None)
    thumb_media_id: str = Field(default="thumb_media_id")
    need_open_comment: Optional[int] = Field(default=1)
    only_fans_can_comment: Optional[int] = Field(default=0)


class Response(BaseModel):
    code: str
    message: str
    data: dict


@router.get("/heartbeat")
def heartbeat():
    logger.info('run heartbeat')
    return 'heartbeat'


@router.post('/generate/image_group')
def get_image_group(
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
    "type_name":'openai',
    "model_select":"gpt-4o"
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
        type_name = request_data.get("type_name", "openai")
        model_select = request_data.get("model_select", "gpt-4o")
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

    # 调用内部逻辑
    try:
        result = travel_generate.images_group(
            images, style, language, length, summary_length, temperature, url, type_name, model_select
        )
        print("travel_generate result:", result)

        if result.get('status', True):  # 如果 status 为 True
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

@router.post('/generate/frame_work')
def get_frame_work(request_data: dict = {
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
    "type_name":'openai',
    "model_select":"gpt-4o"
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
        image_descriptions = request_data.get("image_desc", {})
        type_name = request_data.get("type_name", "openai")
        travel_descriptions=request_data.get("travel_descriptions", "今日武汉夜游，很开心")
        model_select = request_data.get("model_select", "gpt-4o")
        url = request_data.get("url", "http://127.0.0.1:4010/private/inference")
        temperature = request_data.get("temperature", 0.3)
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

    #if not isinstance(image_descriptions, list) or not all(isinstance(desc, str) for desc in image_descriptions):
    #    return Response(
    #        code="400",
    #        message="Invalid image_descriptions format. Must be a list of strings.",
    #        data={}
    #    )

    print("Received theme:", theme)
    print("Received image_descriptions:", image_descriptions)

    # 调用内部逻辑
    try:
        result = travel_generate.generate_travel_frame_work(
            theme=theme, travel_descriptions=travel_descriptions, image_descriptions=image_descriptions, type_name=type_name, model_select=model_select, url=url, temperature=temperature
        )
        print("travel_generate result:", result)

        if result.get('status', True):  # 如果 status 为 True
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

# @router.post('/generate/frame_work_xiaohongshu')
# def get_frame_work(request_data: dict = {
#     "image_desc": {
#         "status":True,
#         "data": {
#                "descriptions": {
#                  "http://smw76g823.hn-bkt.clouddn.com/jpg/bc0e427ef32e4c4ea63e3057a9cb621d.jpg": "这幅图片展示了一座在黄昏时分的现代化斜拉桥的全景视图。天空呈现出从温暖的橙色到深蓝色的渐变色调，暗示着日落时刻。桥梁被点亮，与暮色形成鲜明对比，并反射在下面宁静的水面上，营造出一种镜像效果。桥塔高耸，缆绳将重量分配到支撑结构上。在远处，可以看到一个城市天际线，建筑物点缀着灯光，显示了人类居住和活动的存在。车辆的车灯形成了运动模糊的光轨，表明照片拍摄时车辆在移动。整体氛围宁静而美丽，展示了工程壮举与自然之美之间的和谐融合。",
#                  "http://smw76g823.hn-bkt.clouddn.com/jpg/78caaac2161b47578602fced6409ff57.jpg": "这幅图片展示了一个结合了城市和自然元素的全景景观。在前景，有一条弯曲的道路穿过郁郁葱葱的绿地，几辆汽车在路上行驶，显示出轻度交通流量。道路两侧是高大的树木和灌木，表明这是一个维护良好的公园或林区。中景展示了密集的住宅建筑群，包括多层公寓楼和一些独立的建筑物。这些结构以白色、米色和灰色为主色调，带有红色屋顶，与周围绿植形成对比。背景逐渐过渡到一个更开阔的城市天际线，可见更多高层建筑，天空呈现出淡蓝色，并有粉色云彩的迹象，可能表明这是黎明或黄昏时分。整个场景传达出一种宁静的城市生活感觉，自然环境与城市发展和谐共存。"
#                },
#                "unified_text": "这幅图片展示了一座在黄昏时分的现代化斜拉桥的全景视图。天空呈现出从温暖的橙色到深蓝色的渐变色调，暗示着日落时刻。桥梁被点亮，与暮色形成鲜明对比，并反射在下面宁静的水面上，营造出一种镜像效果。桥塔高耸，缆绳将重量分配到支撑结构上。在远处，可以看到一个城市天际线，建筑物点缀着灯光，显示了人类居住和活动的存在。车辆的车灯形成了运动模糊的光轨，表明照片拍摄时车辆在移动。整体氛围宁静而美丽，展示了工程壮举与自然之美之间的和谐融合。\n\n这幅图片展示了一个结合了城市和自然元素的全景景观。在前景，有一条弯曲的道路穿过郁郁葱葱的绿地，几辆汽车在路上行驶，显示出轻度交通流量。道路两侧是高大的树木和灌木，表明这是一个维护良好的公园或林区。中景展示了密集的住宅建筑群，包括多层公寓楼和一些独立的建筑物。这些结构以白色、米色和灰色为主色调，带有红色屋顶，与周围绿植形成对比。背景逐渐过渡到一个更开阔的城市天际线，可见更多高层建筑，天空呈现出淡蓝色，并有粉色云彩的迹象，可能表明这是黎明或黄昏时分。整个场景传达出一种宁静的城市生活感觉，自然环境与城市发展和谐共存。\n\n这幅图片捕捉到了现代都市生活中宁静的一面。黄昏时分的桥梁，不仅是一座连接城市的纽带，也是一道美丽的风景线。它映射出人类智慧与自然和谐共处的美好愿景。在这片宁静中，我们可以感受到城市的脉动，也能找到内心的平静。这样的景象，不仅让我们欣赏到现代建筑的雄伟，更让我们思考人与自然的关系，如何在发展中保护环境，实现可持续发展。总的来说，这幅图片是一幅美丽而富有启示性的作品，值得我们细细品味和反思。"
#              }
#     },
#     "theme": "武汉之旅",
#     "temperature": 0.3,
#     "type_name":'xinference',
#     "model_select":"MiniCPM-V-2.6-8B"
# }):
#     # 校验 request_data 是否有效
#     if not request_data or not isinstance(request_data, dict):
#         return Response(
#             code="400",
#             message="Invalid request data. Must be a JSON object.",
#             data={}
#         )
#
#     # 从 JSON 数据中提取参数
#     try:
#         theme = request_data.get("theme")
#         image_descriptions = request_data.get("image_desc", {})
#         type_name = request_data.get("type_name", "xinference")
#         model_select = request_data.get("model_select", "MiniCPM-V-2.6-8B")
#         url = request_data.get("url", "http://127.0.0.1:4010/private/inference")
#         temperature = request_data.get("temperature", 0.8)
#     except Exception as e:
#         return Response(
#             code="400",
#             message=f"Invalid request data: {str(e)}",
#             data={}
#         )
#     print('13579:',theme)
#     # 参数校验
#     if not theme or not isinstance(theme, str):
#         return Response(
#             code="400",
#             message="Invalid theme. Must be a non-empty string.",
#             data={}
#         )
#
#     #if not isinstance(image_descriptions, list) or not all(isinstance(desc, str) for desc in image_descriptions):
#     #    return Response(
#     #        code="400",
#     #        message="Invalid image_descriptions format. Must be a list of strings.",
#     #        data={}
#     #    )
#
#     print("Received theme:", theme)
#     print("Received image_descriptions:", image_descriptions)
#
#     # 调用内部逻辑
#     try:
#         result = travel_generate.generate_travel_frame_work_xiaohongshu(
#             theme, image_descriptions, type_name, model_select, url, temperature
#         )
#         print("travel_generate result:", result)
#
#         if result.get('status', False):  # 如果 status 为 True
#             return Response(
#                 code="000000",
#                 message=result.get('message', "Success"),
#                 data=result.get('data', {})
#             )
#         else:
#             return Response(
#                 code="404",
#                 message=result.get('message', "Processing failed"),
#                 data={}
#             )
#     except Exception as e:
#         print("Error in processing:", e)
#         return Response(
#             code="500",
#             message=f"Internal server error: {str(e)}",
#             data={}
#         )
    
@router.post('/generate/travel_result')
def get_travel_result(request_data: dict = 
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
                            "type_name":'openai',
                            "model_select":"gpt-4o"
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
        image_descriptions = request_data.get("image_descriptions", {})
        type_name = request_data.get("type_name", "openai")
        model_select = request_data.get("model_select", "gpt-4o")
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

    #if not isinstance(image_descriptions, {}) or not all(isinstance(desc, str) for desc in image_descriptions):
    #    return Response(
    #        code="400",
    #        message="Invalid image_descriptions format. Must be a list of strings.",
    #        data={}
    #    )

    print("Received theme:", theme)
    print("Received outline:", outline)
    print("Received image_descriptions:", image_descriptions)

    # 调用内部逻辑
    try:
        result = travel_generate.generate_travel_notes(
            theme=theme, outline=outline, image_descriptions=image_descriptions, type_name=type_name, model_select=model_select, url=url,temperature=temperature
        )
        print("travel_generate result:", result)

        if result.get('status', False):  # 如果 status 为 True
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


@router.post('/generate/mark_down')
def get_travel_result(request_data: dict = 
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
                            "type_name":'openai',
                            "model_select":"gpt-4o"
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
        type_name = request_data.get("type_name", "openai")
        model_select = request_data.get("model_select", "gpt-4o")
        temperature = request_data.get("temperature", 0.8)
    except Exception as e:
        return Response(
            code="400",
            message=f"Invalid request data: {str(e)}",
            data={}
        )

    # 调用内部逻辑
    url="http://127.0.0.1:4010/private/inference"
    try:
        result = travel_generate.generate_markdown_article(
            data,temperature=temperature, img_width=img_width, url=url, type_name=type_name, model_select=model_select
        )
        print(result)

        if result.get('status', True):  # 如果 status 为 True
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

def extract_and_parse_json(input_text):
    """
    从文本中提取 JSON 字符串并解析为 JSON 对象。

    Args:
        input_text (str): 输入的包含 JSON 字符串和其他文本的混合内容。

    Returns:
        dict or list: 提取出的 JSON 对象，或 None 如果未找到有效 JSON。
    """
    try:
        # 匹配 JSON 字符串的正则表达式
        json_pattern = re.compile(r'\{.*?\}|\[.*?\]', re.DOTALL)
        
        # 搜索第一个匹配的 JSON 字符串
        match = json_pattern.search(input_text)
        
        if match:
            # 提取匹配的 JSON 字符串
            json_string = match.group()
            print("提取的 JSON 字符串:", json_string)
            
            # 转换为 JSON 对象
            return json.loads(json_string)
        else:
            print("未找到 JSON 字符串")
            return None
    except json.JSONDecodeError as e:
        print("JSON 解析错误:", e)
        return None
    
@router.post('/generate/md2json')
def md2json_test(request_data: dict =
                      {
                            "markdown_file":"travel_notes_content",
                            "temperature": 0.3,
                            "type_name":'openai',
                            "model_select":"gpt-4o"
                        }):
    # 从 JSON 数据中提取参数
    try:
        markdown_file = request_data.get("markdown_file")
        type_name = request_data.get("type_name", "openai")
        model_select = request_data.get("model_select", "gpt-4o")
        url = request_data.get("url", "http://127.0.0.1:4010/private/inference")
        temperature = request_data.get("temperature", 0.8)
    except Exception as e:
        logger(e)

    #try:
    result = travel_generate.md2json_new(markdown_file,temperature=temperature, url=url, type_name=type_name, model_select=model_select)
    #try:
    result=result.replace('https:','http:')
    # 使用正则提取第一个{ 到最后一个}的内容
    match = re.search(r'\{.*\}', result, re.DOTALL)
    print('-+-=---')
    print(match)
    if match:
        json_content = match.group()
        try:
            # 将提取的内容转换为JSON格式
            json_data = json.loads(json_content)
            print(json.dumps(json_data, indent=4, ensure_ascii=False))
        except json.JSONDecodeError as e:
            json_data=json_content
            print(f"JSON解析错误: {e}")
    else:
        print("未找到匹配的JSON内容")
    print('start:----------')
    print(json_data)
    #json_output=json.loads(result_tmp1)
    json_output = json_data
    #print(json_output)
    #except Exception as e:
    #    json_output=extract_and_parse_json(result)
    #    print(json_output)
    #    # 保存 JSON 到文件
    #    output_file = "travel_notes.json"
    #    with open(output_file, "w", encoding="utf-8") as file:
    #        file.write(result)
    #    print(f"JSON 已保存到 {output_file}")
    print(type(json_output))
    return Response(
            code="000000",
            message="Success",
            data=json_output)


    #except Exception as e:
    #    logger(e)





