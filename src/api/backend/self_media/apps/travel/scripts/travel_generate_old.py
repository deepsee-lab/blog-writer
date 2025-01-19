from pydantic import BaseModel
import re,requests,os,base64
from PIL import Image
from server.self_media.apps.travel.scripts.model_run import model_rag
from loguru import logger
import traceback

class Response(BaseModel):
    code: str
    message: str
    data: dict

def compress_image(image_path, output_path=None, max_size_kb=1024):
    """
    压缩图片到指定大小以下（默认小于1024KB）。
    参数:
        image_path: 本地图片路径
        output_path: 压缩后图片的保存路径（为空时自动生成）
        max_size_kb: 压缩目标大小（单位：KB）
    返回:
        压缩后的图片路径
    """
    # 自动生成 output_path（如果为空）
    if not output_path:
        base_name, ext = os.path.splitext(os.path.basename(image_path))
        output_path = f"{base_name}_compressed.jpg"

    # 打开图片
    img = Image.open(image_path)

    # 初始化压缩参数
    quality = 99  # 初始质量
    while True:
        # 保存图片到指定路径
        img.save(output_path, format="JPEG", quality=quality)

        # 检查文件大小
        file_size_kb = os.path.getsize(output_path) / 1024  # 转换为 KB
        if file_size_kb <= max_size_kb:
            print(f"图片压缩成功，最终大小：{file_size_kb:.2f}KB")
            break  # 如果文件大小小于等于目标大小，停止压缩
        quality -= 3  # 每次降低质量
        if quality < 3:  # 防止质量过低
            print(f"无法将图片压缩到小于 {max_size_kb}KB，当前大小：{file_size_kb:.2f}KB")
            break

    return output_path

def analyze_image(image=None, style="自然流畅", language="中文", length="200", temperature=0.3,url='http://127.0.0.1:4010/private/inference',type_name='openai',model_select='gpt-4o'):
    """
    调用 OpenAI API 对图片进行分析，生成描述。
    参数: 
        image: 图片的 URL 或本地路径
        style: 描述风格
        language: 描述语言
        length: 描述字数
        temperature: 控制生成的随机性
    """
    #if re.match(r'^http', image):  # 判断是否为 URL
    #    response = requests.get(image, stream=True)
    #    if response.status_code == 200:
    #        temp_path = "temp_image.jpg"
    #        with open(temp_path, "wb") as temp_file:
    #            temp_file.write(response.content)
    #        image_path = temp_path
    #    else:
    #        raise ValueError("无法下载网络图片，请检查 URL 是否正确。")
    #else:  # 本地图片路径
    #    image_path = image
#
    #file_size_kb = os.path.getsize(image_path) / 1024
    #if file_size_kb > 1024:
    #    image_path = compress_image(image_path)
#
    #with open(image_path, 'rb') as img_file:
    #    image_base = base64.b64encode(img_file.read()).decode('utf-8')
    #images = f"data:image/jpeg;base64,{image_base}"

    try:
        query=[
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image
                            }
                        },
                        {
                            "type": "text",
                            "text": f"请用{style}的风格，用{language}语言描述照片，直接描述，不带这张照片或画面中等字样，字数为{length}。"
                        }
                    ]
        messages=[
            {
                "role":"user",
                "content":query
            }
        ]
        response = model_rag(url,messages,type_name,model_select)
        print(response)
        tempdata = response['data']
        logger.info(f'response11111{tempdata}')
        if response['code']==200 :
            return {"status": True, "data": response['data']}
        else:
            return {"status": False, "data": "图片分析失败，请检查 API 响应。"}
    except Exception as e:
        logger.info(traceback.print_exc())
        return {"status": False, "data": f"图片分析失败，错误信息: {str(e)}"}
    finally:
        print('heello world')
        #if re.match(r'^http', image):
        #    os.remove(temp_path)

def images_group(images=None, style="自然流畅", language="中文", length="200", summary_length="400",temperature=0.8,url='http://127.0.0.1:4010/private/inference',type_name='openai',model_select='gpt-4o'):
    """
    分析图片列表（支持本地路径和 URL），生成每张图片的描述，并返回统一格式的结果。
    参数:
        images: 图片路径列表（可以是本地路径或 URL）
        style: 描述风格
        language: 描述语言
        length: 每张图片描述的总字数
        summary_length: 最终生成的长文字数
        temperature: 控制生成的随机性
    返回:
        包含所有图片描述的字典，形式为 {status: True, data: {image_path1: content}}
    """
    if not images or not isinstance(images, list):
        return {"status": False, "data": "输入的 images 参数无效，请提供图片路径或 URL 列表。"}

    # 分析每张图片
    descriptions = {}
    description_texts = []  # 用于存储所有图片的描述文本
    for image in images:
        logger.info(f"正在分析图片：{image}")
        try:
            result = analyze_image(image=image, style=style, language=language, length=length, temperature=temperature,url=url,type_name=type_name,model_select=model_select)
            if result["status"]:
                descriptions[image] = result["data"]
                description_texts.append(result["data"])
            else:
                return {
                    'status':False,
                    'message':f"分析失败：{result['data']}"
                }
        except Exception as e:
            descriptions[image] = f"分析失败：{str(e)}"
            return {
                    'status':False,
                    'message':f"分析失败：{str(e)}"
                }

    # 将所有描述统一风格并生成长文
    try:
        temp = chr(10).join(description_texts) 
        logger.info('temp', temp)
        query=f"以下是多张图片的描述：\n\n{temp}\n\n请将这些描述统一为{style}风格，用{language}语言，生成一段连贯的文字，字数为{summary_length}，并总结感想，升华文字。"
        messages=[
            {
                "role":"user",
                "content":query
            }
        ]
        unified_text = model_rag(url,messages,type_name,model_select)
        if unified_text['code']==200 :
            return {"status": True, "data": {"descriptions": descriptions, "unified_text": unified_text['data']},'message':'success'}
        else:
            return {"status": False, "message": "描述风格统一失败，请检查 API 响应。"}
    except Exception as e:
        logger.info(traceback.print_exc())
        return {"status": False, "message": f"描述风格统一失败，错误信息: {str(e)}"}
    

def generate_travel_frame_work(theme, image_descriptions,type_name,model_select,url,temperature):
    """
    使用 OpenAI 的 GPT 模型生成旅游札记。
    参数:
        theme: 游记主题（如果为 None，则由模型生成）
        image_descriptions: 图片描述列表，每个描述对应一个章节
    返回:
        包含标题和大纲的字典，形式为:
        {
            "status": true,
            "data": {
                "title": "游记标题",
                "outline": "游记大纲",
                "content": "完整游记正文"
            }
        }
    """
    descriptions = image_descriptions.get("descriptions", {})
    # print(descriptions)

    # 如果 theme 为 None，则生成一个标题
    if not theme:
        try:
            query=f"以下是几段图片描述：\n\n{chr(10).join(image_descriptions)}\n\n请根据这些描述生成一个适合的游记标题。"
            messages=[
            {
                "role":"user",
                "content":query
            }
        ]
            result = model_rag(url,messages,type_name,model_select)
            if result['code']==200 :
                theme = result['data'].strip()
            else:
                return {"status": False, "message": "标题生成失败，请检查 API 响应。"}
        except Exception as e:
            return {"status": False, "message": f"标题生成失败，错误信息: {str(e)}"}

    # 根据图片描述生成游记大纲和正文

    try:
        query=f"主题是：{theme}\n以下是几段图片描述：\n\n{chr(10).join(descriptions)}\n\n请根据这些描述生成一个游记大纲，并写一篇完整的游记，包括介绍、正文（每段描述作为一个章节）和总结。"
        messages=[
            {
                "role":"user",
                "content":query
            }
        ]
        result = model_rag(url,messages,type_name,model_select,temperature)

        if result['code']==200 :
            content = result['data'].strip()
            return {
                "status": True,
                'message':'success',
                "data": {
                    "title": theme,
                    "outline": "根据正文内容提取的大纲",
                    "content": content
                }
            }
        else:
            return {"status": False, "message": "游记生成失败，请检查 API 响应。"}
    except Exception as e:
        return {"status": False, "message": f"游记生成失败，错误信息: {str(e)}"}


def generate_travel_notes(theme, outline, image_descriptions,type_name,model_select,url,temperature):
    """
    根据主题、大纲和图片描述生成完整的游记

    参数:
        theme (str): 游记主题/标题
        outline (list): 游记大纲列表
        image_descriptions (dict): 包含图片描述数据的字典
    """
    try:
        # 提取有效的图片描述
        descriptions = image_descriptions["data"].get("descriptions", {})
        valid_descriptions = []
        image_paths = {
            'network': [],  # 存储网络图片URL
            'local': []  # 存储本地图片路径
        }
        print('1234')
        for img_path, desc in descriptions.items():
            if isinstance(desc, str) and "分析失败" not in desc:
                # 判断是否为网络图片URL
                is_url = img_path.startswith(('http://', 'https://'))

                valid_descriptions.append({
                    "path": img_path,
                    "description": desc,
                    "is_url": is_url
                })

                # 分类存储图片路径
                if is_url:
                    image_paths['network'].append(img_path)
                else:
                    # 统一路径分隔符为正斜杠
                    local_path = img_path.replace('\\', '/')
                    image_paths['local'].append(local_path)
        print('456')
        if not valid_descriptions:
            return {"status": False, "message": "没有有效的图片描述"}

            # 获取统一文本
        unified_text = image_descriptions.get('unified_text', '')

        # 构建提示文本，改进大纲格式
        outline_text = "\n".join([f"{i + 1}. {item}" for i, item in enumerate(outline)])

        # 组合场景描述
        scene_descriptions = []
        if unified_text:
            scene_descriptions.append("整体场景描述：")
            scene_descriptions.append(unified_text)
            scene_descriptions.append("\n具体场景细节：")

        for desc in valid_descriptions:
            scene_descriptions.append(f"- {desc['description']}")

        combined_descriptions = "\n".join(scene_descriptions)

        prompt = f"""  
请根据以下信息生成一篇完整的游记：  

标题：{theme}  

大纲：  
{outline_text}  

场景描述：  
{combined_descriptions}  

要求：  
1. 按照给定大纲组织文章结构  
2. 将场景描述自然地融入相应章节  
3. 保持文章流畅性和连贯性  
4. 加入个人感受和思考  
5. 在开头添加引言，结尾添加总结  
6. 使用优美生动的语言  
7. 每个部分要有适当的过渡  
8. 突出主题特色  
"""

        # 调用模型生成游记
        messages=[
            {
                    "role": "system",
                    "content": "你是一位专业的旅行文章作家，擅长将照片和文字结合，创作生动有趣的游记。"
                },
                {
                    "role": "user",
                    "content": prompt
                }
        ]
        result = model_rag(url,messages,type_name,model_select,temperature)

        if result['code']==200:
            travel_notes = result['data'].strip()

            # 构建返回结果
            result = {
                "status": True,
                "message":"success",
                "data": {
                    "title": theme,
                    "outline": outline,
                    "content": travel_notes,
                    "images": {
                        "network": image_paths['network'],  # 网络图片URL列表
                        "local": image_paths['local']  # 本地图片路径列表
                    },
                    "unified_text": unified_text,
                    "descriptions": [
                        {
                            "path": desc["path"],
                            "description": desc["description"],
                            "is_url": desc["is_url"]
                        } for desc in valid_descriptions
                    ]
                }
            }
            return result
        else:
            return {"status": False, "message": "游记生成失败，请检查API响应。"}

    except Exception as e:
        return {"status": False, "message": f"游记生成失败，错误信息: {str(e)}"}

def generate_markdown_article(result, temperature,img_width=600,url='http://127.0.0.1:4010/private/inference',type_name='openai',model_select='gpt-4o'):
    """
    根据游记生成结果生成纯Markdown格式文档并保存到本地

    参数:
        result (dict): generate_travel_notes 函数的返回结果
        output_path (str): 输出文件路径
        img_width (int): 图片显示宽度
    """
    try:

        data = result
        descriptions = data["descriptions"]

        # 准备图片信息文本
        image_info = []
        for desc in descriptions:
            path = desc["path"]
            description = desc["description"]
            # 使用正确的Markdown图片语法
            image_info.append(f"![{description}]({path})")

        image_text = "\n".join(image_info)

        # 构建提示文本
        prompt = f"""  
请将以下游记内容转换为纯Markdown格式文本，并在适当的位置插入图片。  

原始内容：  
{data['content']}  

图片描述：
{data['descriptions']}

可用图片：  
{image_text}  

要求：  
1. 保持原文的结构和内容  
2. 在每个章节的相关描述后插入对应的图片  
3. 使用HTML格式的img标签来设置图片宽度：<img src="图片路径" alt="描述" width="{img_width}">  
4. 确保图片位置与内容相关  
5. 保持文章的流畅性  
6. 适当添加分隔符或空行  
7. 对于本地图片和网络图片都使用相同的格式  
8. 保持原有的标题层级结构  
9. markdown不要添加多余的空行，不要多余的描述，打开文档即是精美的游记
"""

        # 调用模型生成Markdown文本
        messages=[
                {
                    "role": "system",
                    "content": "你是一位精通Markdown格式的技术文档专家，擅长组织文章结构和图文排版。"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        result = model_rag(url,messages,type_name,model_select,temperature)

        if result['code']==200 :
            markdown_content = result['data'].strip()
            print(markdown_content)
            markdown_content = markdown_content.replace("```markdown", "").replace("```", "")
            # 构建返回结果
            result = {
                "status": True,
                "data": {
                    "title": data["title"],
                    "markdown_content": markdown_content,
                    "images": data["images"]
                }
            }
            return result
        else:
            return {"status": False, "data": "Markdown生成失败，请检查API响应。"}

    except Exception as e:
        return {"status": False, "data": f"Markdown生成失败，错误信息: {str(e)}"}

def generate_travel_frame_work_xiaohongshu(theme, image_descriptions,type_name,model_select,url,temperature):
    """
    使用 OpenAI 的 GPT 模型生成旅游札记。
    参数:
        theme: 游记主题（如果为 None，则由模型生成）
        image_descriptions: 图片描述列表，每个描述对应一个章节
    返回:
        包含标题和大纲的字典，形式为:
        {
            "status": true,
            "data": {
                "title": "游记标题",
                "outline": "游记大纲",
                "content": "完整游记正文"
            }
        }
    """
    descriptions = image_descriptions.get("descriptions", {})
    # print(descriptions)

    # 如果 theme 为 None，则生成一个标题
    if not theme:
        try:
            query=f"以下是几段图片描述：\n\n{chr(10).join(image_descriptions)}\n\n请根据这些描述生成一个适合的游记标题。"
            messages=[
            {
                "role":"user",
                "content":query
            }
        ]
            result = model_rag(url,messages,type_name,model_select)
            if result['code']==200 :
                theme = result['data'].strip()
            else:
                return {"status": False, "message": "标题生成失败，请检查 API 响应。"}
        except Exception as e:
            return {"status": False, "message": f"标题生成失败，错误信息: {str(e)}"}

    # 根据图片描述生成游记大纲和正文

    try:
        gongzhonghao_prompt1='''你是一名专业的微信公众号旅行博主，擅长撰写优质的旅行札记。你的任务是根据我的提示词或描述生成微信公众号风格的旅行文章。文章需要具备以下特点：
                        标题吸引人：标题要有创意，能够抓住读者的眼球，适当使用数字、悬念或情感化的表达。
                        语言优美且生动：文字要有画面感，注重细节描写，能够让读者身临其境。
                        结构清晰：文章分为以下部分：
                        引言：简要介绍旅行的背景、目的地或主题，吸引读者兴趣。
                        正文：分段叙述旅行的过程，每段围绕一个场景或主题展开，包含具体的细节、感受和故事。
                        总结：总结旅行的感悟或收获，给读者留下深刻印象。
                        适当融入个人体验：分享自己的真实感受、旅行中的趣事或小插曲，增加文章的真实性和亲切感。
                        实用性：适当提供旅行建议或攻略（如交通、住宿、美食推荐等），让读者觉得文章有参考价值。
                        排版友好：段落简洁，适当使用小标题、列表或分点，方便读者阅读。
                        情感共鸣：通过文字传递旅行的意义或情感，让读者感受到旅行的美好与独特。
                        请根据以上要求撰写旅行札记，最后生成适合微信公众号的相关标签。'''
        query=f"主题是：{theme}\n以下是几段图片描述：\n\n{chr(10).join(descriptions)}\n\n请根据这些描述生成一个游记大纲，并写一篇完整的游记，包括介绍、正文（每段描述作为一个章节）和总结。"
        messages=[
            {
                    "role": "system",
                    "content": (
                        gongzhonghao_prompt1
                    )
            },
            {
                "role":"user",
                "content":query
            }
        ]
        result = model_rag(url,messages,type_name,model_select,temperature)

        if result['code']==200 :
            content = result['data'].strip()
            return {
                "status": True,
                'message':'success',
                "data": {
                    "title": theme,
                    "outline": "根据正文内容提取的大纲",
                    "content": content
                }
            }
        else:
            return {"status": False, "message": "游记生成失败，请检查 API 响应。"}
    except Exception as e:
        return {"status": False, "message": f"游记生成失败，错误信息: {str(e)}"}