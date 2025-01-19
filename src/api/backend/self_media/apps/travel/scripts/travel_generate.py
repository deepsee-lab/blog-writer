from pydantic import BaseModel
import re,requests,os,base64
from PIL import Image
from apps.travel.scripts.model_run import model_rag
from loguru import logger
import traceback
import json

class Response(BaseModel):
    code: str
    message: str
    data: dict

# client = OpenAI(
#     base_url=os.getenv('OPEN_API_BASE'),
#     api_key=os.getenv('OPEN_API_KEY'),
# )
# 从环境变量中获取API密钥和基础URL
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), base_url=os.getenv("OPENAI_BASE_URL"))






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
    if re.match(r'^http', image):  # 判断是否为 URL
        response = requests.get(image, stream=True)
        if response.status_code == 200:
            temp_path = "temp_image.jpg"
            with open(temp_path, "wb") as temp_file:
                temp_file.write(response.content)
            image_path = temp_path
        else:
            raise ValueError("无法下载网络图片，请检查 URL 是否正确。")
    else:  # 本地图片路径
        image_path = image

    file_size_kb = os.path.getsize(image_path) / 1024
    if file_size_kb > 1024:
        image_path = compress_image(image_path)

    with open(image_path, 'rb') as img_file:
        image_base = base64.b64encode(img_file.read()).decode('utf-8')
    images = f"data:image/jpeg;base64,{image_base}"

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

def generate_travel_frame_work(theme,travel_descriptions, image_descriptions, url='http://127.0.0.1:4010/private/inference',type_name='openai',model_select='gpt-4o',temperature=0.3):
    """url='http://127.0.0.1:4010/private/inference',type_name='openai',model_select='gpt-4o'
    使用 OpenAI 的 GPT 模型生成旅游札记。
    参数:
        theme: 游记主题（如果为 None，则由模型生成）
        travel_descrptions: 用户对游记的写作要求
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
    if not image_descriptions.get("status") or "data" not in image_descriptions:
        return {"status": False, "data": "图片描述数据无效。"}

    descriptions = image_descriptions["data"].get("descriptions", {})
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
    json_prompt='''
    请生成一个游记的大纲，并确保输出是严格的 JSON 格式（非字符串），直接以 JSON 数据返回，符合以下结构：subtitle是章节标题（数量和输出图片数量一致），content是章节内容，image_path是图片路径：
    {
  "title": "游记标题",
  "introduction": {
    "content": "游记介绍",
  },
  "body": [
    {
      "subtitle": "subtitle_string",
      "content": "content_string",
      "image_path": "image_path"
    },
    {
      "subtitle": "subtitle_string",
      "content": "content_string",
      "image_path": "image_path"
    },
    {
      "subtitle": "subtitle_string",
      "content": "content_string",
      "image_path": "image_path"
    }
  ],
  "conclusion": {
    "content": "游记总结"
  },
  "tags": [
    "标签1",
    "标签2",
    "标签3",
    "标签4",
    "标签5"
  ]
}
    '''
    xiaohongshu_prompt='''你是一名小红书博主，你的任务是根据我的提示词或描述生成小红书风格的文案："
                        "包括标题和内容。你的文案应该有以下特点：表达要口语化，标题吸引人，"
                        "要多使用 emoji 表情图标，内容观点尽量分点罗列，适当描述自己的使用体验和评价，"
                        "文案最后生成相关的标签。
                        作为多才多艺的小红书专业文案撰写师，你同样也是品牌策略专家/创意专家/文案撰写专家/传播效果专家/消费者洞察专家/竞品分析专家，拥有丰富的品牌策略和小红书写作经验。
                        你的任务是撰写小红书笔记，包括标题、正文、行动号召以及图片建议。基于笔记的内容、结构和表达，对它们进行评分并给出优化建议。
                        深刻理解优秀小红书笔记的核心要素。 能够理解小红书笔记的关键内容。 有能力分析文案的表达、逻辑和吸引力。'''
    gongzhonghao_prompt='''你是一名专业的微信公众号旅行博主，擅长撰写优质的旅行札记。你的任务是根据我的提示词或描述生成微信公众号风格的旅行文章。文章需要具备以下特点：
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
    try:
        query=f"主题是：{theme}\n以下是几段图片描述：\n\n{chr(10).join(descriptions)}\n\n请根据这些描述生成一个游记大纲，包括介绍、正文（每段描述作为一个章节）和总结。"
        messages=[
            {
                "role":"system",
                "content":json_prompt,
            },
            {
                "role": "system",
                "content": xiaohongshu_prompt,
            },
            {
                "role": "user",
                "content": query
            },
            {
                "role": "user",
                "content": f"以下是用户对游记的写作要求：\n\n{travel_descriptions}\n\n请根据这些要求生成游记大纲。"
            }
        ]
        result = model_rag(url,messages,type_name,model_select,temperature)

        if result['code']==200 :
            content = result['data'].strip()
            try:
                content=json.loads(content)
            except Exception as e:
                content=content
                print(f'content 转json错误:{e}')
                print(content)
                print('------------')
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


def generate_travel_notes(theme, outline, image_descriptions,url='http://127.0.0.1:4010/private/inference',type_name='openai',model_select='gpt-4o',temperature=0.3):
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
        messages = [
            {
                "role": "system",
                "content": "你是一位专业的旅行文章作家，擅长将照片和文字结合，创作生动有趣的游记。"
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
        result = model_rag(url, messages, type_name, model_select, temperature)

        if result['code'] == 200:
            travel_notes = result['data'].strip()

            # 构建返回结果
            result = {
                "status": True,
                "message": "success",
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
9. 在文档开头添加图片样式设置  
10. markdown不要添加多余的空行，不要多余的描述，打开文档即是精美的游记
"""

        # 调用模型生成Markdown文本
        messages = [
            {
                "role": "system",
                "content": "你是一位精通Markdown格式的技术文档专家，擅长组织文章结构和图文排版。"
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
        result = model_rag(url, messages, type_name, model_select, temperature)

        if result['code'] == 200:
            markdown_content = result['data'].strip()
            print(markdown_content)
            markdown_content = markdown_content.strip("```mardkdown").strip("```").strip()
            final_markdown = f"""<style>  
img {{  
  width: {img_width}px;  
  max-width: 100%;  
  height: auto;  
}}  
</style>  

{markdown_content}  
"""

            # 保存到文件
            output_path = "travel_notes.md"
            try:
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(final_markdown)
            except Exception as e:
                return {"status": False, "data": f"Markdown保存失败，错误信息: {str(e)}"}
            # 构建返回结果
            result = {
                "status": True,
                "data": {
                    "title": data["title"],
                    "markdown_content": final_markdown,
                    "images": data["images"]
                }
            }
            return result
        else:
            return {"status": False, "data": "Markdown生成失败，请检查API响应。"}

    except Exception as e:
        return {"status": False, "data": f"Markdown生成失败，错误信息: {str(e)}"}


def md2json_new(markdown_text="travel_notes", temperature=0.3 ,url='http://127.0.0.1:4010/private/inference',type_name='openai',model_select='gpt-4o'):

    # 读取 Markdown 文件内容
    #with open(markdown_file, "r", encoding="utf-8") as file:
    #    markdown_text = file.read()

        # 定义 Prompt
    prompt = f"""  
    将以下 Markdown 文本转换为 JSON 格式，JSON 的结构如下：  
    {{  
      "title": "value",  
      "文章": {{  
        "摘要": "value",  
        "正文": [  
          {{  
            "text": "value",  
            "img": "url || 空"  
          }}  
        ]  
      }}  
    }}  

    Markdown 文本如下：  
    {markdown_text}  
    """
    messages = [
        {
            "role": "system",
            "content": ""
        },
        {
            "role": "user",
            "content": prompt
        }
    ]
    # 调用 GPT-4 API
    result = model_rag(url, messages, type_name, model_select, temperature)

    if result['code'] == 200:
        json_output = result['data'].strip("```json").strip("```").strip()
        print(json_output)
        try:
            # 1. 替换 https: 为 http:
            step1 = re.sub(r'https:', 'http:', json_output)

            # 2. 将 2 个或更多 # 替换为空
            step12 = re.sub(r'#{2,}', '', step1)

            final_output = re.sub(r'*{2,}', '', step12)
        except Exception as e:
            print(f"去：符号报错l : {e}")
            final_output=json_output

        print(f'替换后：{final_output}')
        # 保存 JSON 到文件
        output_file = "travel_notes.json"
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(final_output)
        print(f"JSON 已保存到 {output_file}")
        return final_output

def md2json(markdown_file="travel_notes.md", temperature=0.3 ,url='http://127.0.0.1:4010/private/inference',type_name='openai',model_select='gpt-4o'):

    # 读取 Markdown 文件内容
    with open(markdown_file, "r", encoding="utf-8") as file:
        markdown_text = file.read()

        # 定义 Prompt
    prompt = f"""  
    将以下 Markdown 文本转换为 JSON 格式，JSON 的结构如下：  
    {{  
      "title": "value",  
      "文章": {{  
        "摘要": "value",  
        "正文": [  
          {{  
            "text": "value",  
            "img": "url || 空"  
          }}  
        ]  
      }}  
    }}  

    Markdown 文本如下：  
    {markdown_text}  
    """
    messages = [
        {
            "role": "system",
            "content": ""
        },
        {
            "role": "user",
            "content": prompt
        }
    ]
    # 调用 GPT-4 API
    result = model_rag(url, messages, type_name, model_select, temperature)

    if result['code'] == 200:
        json_output = result['data'].strip("```json").strip("```").strip()
        print(json_output)
        # 保存 JSON 到文件
        output_file = "travel_notes.json"
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(json_output)
        print(f"JSON 已保存到 {output_file}")
        return json_output


if __name__ == '__main__':
    # main()

    ###函数测试 analyze_image()
    # print(analyze_image(r"E:\llmweibo\multimodal20241113\img\wuhan\compress\compressed_俯瞰城市公园.jpg"))   ###本地图片解析
    # print(analyze_image("http://smies7nqa.hd-bkt.clouddn.com/wuhan/%E5%9F%8E%E5%B8%82%E5%BB%BA%E7%AD%91%E5%A4%9C%E6%99%AF%E7%BE%8E%E5%9B%BE.jpg"))   ###图片过大无法解析
    # print(analyze_image("http://smw76g823.hn-bkt.clouddn.com/a_cute_rabbit_eat_gross_20240901_161237.512563.png"))   ###解析网络图片

    ###函数测试 compress_image()
    # result = compress_image(r"E:\llmweibo\multimodal20241113\img\wuhan\compress\compressed_俯瞰城市公园.jpg")
    # result=compress_image("http://smies7nqa.hd-bkt.clouddn.com/wuhan/%E5%9F%8E%E5%B8%82%E5%BB%BA%E7%AD%91%E5%A4%9C%E6%99%AF%E7%BE%8E%E5%9B%BE.jpg")

    ###analyze_image()与compress_image()结合使用
    # print(analyze_image(r"E:\llmweibo\multimodal20241113\img\wuhan\compress\compressed_俯瞰城市公园_compressed.jpg"))
    # print(analyze_image("http://smies7nqa.hd-bkt.clouddn.com/wuhan/%E5%9F%8E%E5%B8%82%E5%BB%BA%E7%AD%91%E5%A4%9C%E6%99%AF%E7%BE%8E%E5%9B%BE.jpg"))
    # print(analyze_image(r"D:\BaiduNetdiskDownload\武汉实拍图片\武汉实拍图片\武汉黄昏东湖汉秀剧场全景(1).jpg"))

    ##images_group()函数测试：本地文件夹或列表
    # print(images_group(r"E:\llmweibo\multimodal20241113\img\wuhan\compress"))
    # image_descriptions = images_group(
    #     images=[
    #         "D:\llmweibo\multimodal20241113\img\wuhan\compress\compressed_傍晚武汉国际广场.jpg",
    #         "D:\llmweibo\multimodal20241113\img\wuhan\compress\compressed_城市建筑夜景美图.jpg",
    #         "D:\llmweibo\multimodal20241113\img\wuhan\compress\compressed_登高俯瞰武汉黄昏.jpg",
    #         "D:\llmweibo\multimodal20241113\img\wuhan\compress\compressed_热干面.jpg",
    #     ],
    #     style="自然流畅",
    #     language="中文",
    #     length="200",
    #     summary_length="1000",
    #     temperature=0.3
    # )
    # print("image_descriptions:", image_descriptions)
    # print("image_descriptions.data.dscriptions",image_descriptions['data']['descriptions'])


    # image_descriptions={'status': True, 'data': {'descriptions': {'http://smies7nqa.hd-bkt.clouddn.com/wuhan/%E5%9F%8E%E5%B8%82%E5%BB%BA%E7%AD%91%E5%A4%9C%E6%99%AF%E7%BE%8E%E5%9B%BE.jpg': '夜幕降临，城市的灯光逐渐亮起，展现出一片璀璨的景象。建筑物的灯光设计独具匠心，尤其是中央那座高耸的建筑，形状如同一个巨大的花瓶，顶部微微倾斜，灯光在其表面流动，呈现出梦幻般的色彩。周围的建筑物也被灯光勾勒出轮廓，形成一幅现代都市的画卷。远处的天际线与近处的建筑群相映成趣，天空的颜色从深蓝渐变为浅紫，给人一种宁静而又充满活力的感觉。道路上的车辆川流不息，车灯如同流动的星河，点缀着城市的夜色。绿化带和水池在灯光的映衬下显得格外柔和，为整个城市增添了一抹自然的气息。整体氛围既现代又富有生机，展现出城市在夜晚的独特魅力。', 'http://smies7nqa.hd-bkt.clouddn.com/wuhan/武汉光谷德国风情街风景.jpg': '建筑物呈现出欧洲风格，拥有尖顶和精美的雕刻装饰，给人一种古典而庄重的感觉。建筑外墙是浅黄色的石材，窗户排列整齐，显得大气而典雅。正中间有一个大型电子屏幕，显示着CGV影城的IMAX广告，吸引着路人的目光。下方是一个开放的广场，地面铺设着整齐的石板，中央有一个喷泉，水柱在阳光下闪烁着晶莹的光芒。广场周围有一些商铺，门面装饰着绿色条纹的遮阳篷，营造出一种休闲的购物氛围。几面蓝白相间的旗帜悬挂在建筑之间，增添了几分活力。人们在广场上悠闲地散步，有的在喷泉边驻足欣赏，有的在商店门口流连。几棵棕榈树点缀其间，给这个现代化的商业区增添了一丝热带风情。整体环境显得既繁华又舒适，是一个集购物、娱乐和休闲于一体的理想场所。', 'E:\\llmweibo\\multimodal20241113\\img\\wuhan\\compress\\compressed_俯瞰城市公园_compressed.jpg': '湖泊宁静而美丽，湖水呈现出清澈的蓝绿色，倒映着岸边的树木和建筑。湖边坐落着一座传统的中式建筑，屋顶是典型的飞檐翘角，显得古色古香。建筑周围绿树成荫，树木郁郁葱葱，给人一种清新自然的感觉。湖的对岸可以看到一些建筑物和设施，似乎是一个游乐场或休闲区，色彩鲜艳，增添了活力。湖面上有几座小亭子，亭子设计精巧，结构对称，与周围的自然景观和谐相融。远处的村庄点缀在绿色的背景中，红色的屋顶与周围的绿色形成鲜明对比，显得格外醒目。整体景色宁静而和谐，展现出一种悠闲和谐的生活氛围，仿佛是一个可以让人放松心情的好地方。'}, 'unified_text': '夜幕降临，城市的灯光逐渐亮起，展现出一片璀璨的景象。中央那座高耸的建筑形如巨大的花瓶，顶部微微倾斜，灯光在其表面流动，呈现出梦幻般的色彩，成为城市夜空中最耀眼的存在。周围的建筑物在灯光的勾勒下，形成一幅现代都市的画卷。深蓝到浅紫的天空，与近处的建筑群相映成趣，宁静中透着活力。道路上的车辆川流不息，车灯如同流动的星河，点缀着城市的夜色。绿化带和水池在灯光的映衬下显得格外柔和，为城市增添了一抹自然的气息。\n\n与此同时，城市的一角展现出欧洲风格的建筑，尖顶和精美的雕刻装饰，古典而庄重。浅黄色石材的外墙，整齐排列的窗户，显得大气典雅。大型电子屏幕上滚动的IMAX广告，吸引着路人的目光。开放的广场中央，喷泉在阳光下闪烁着晶莹的光芒。商铺门面装饰着绿色条纹的遮阳篷，营造出休闲的购物氛围。几面蓝白相间的旗帜在建筑之间飘扬，增添了几分活力。人们在广场上悠闲地散步，享受着繁华与舒适。\n\n远离城市的喧嚣，湖泊宁静而美丽，湖水清澈的蓝绿色倒映着岸边的树木和建筑。湖边的中式建筑，飞檐翘角，古色古香，周围绿树成荫，清新自然。湖对岸的游乐场或休闲区，色彩鲜艳，增添了活力。湖面上的小亭子，设计精巧，与自然景观和谐相融。远处的村庄，红色屋顶与绿色背景形成鲜明对比，格外醒目。整体景色宁静和谐，展现出悠闲的生活氛围。\n\n这些景象共同描绘出一个既现代又富有生机的城市画卷，展现了人类与自然、传统与现代的完美融合。在这片土地上，繁华与宁静并存，历史与未来交织，生活的多样性和丰富性在此展现无遗。无论是城市的璀璨夜景，还是湖畔的宁静美景，都让人感受到生活的美好与希望。'}}

    # with open("image_descriptions.json", "r", encoding="utf-8") as json_file:
    #     image_descriptions = json.load(json_file)
    # print(image_descriptions['data']['descriptions'])
    #
    # # ###测试函数
    # # outline_result = generate_travel_frame_work("灯火阑珊处，武汉夜色美", "我在武汉游玩了一天，去了武汉国际广场、欣赏了城市夜景，品尝了热干面。请写一段轻松明快的游记", image_descriptions)
    # # print(outline_result['data']['content'])
    # #
    # outline_result = generate_travel_frame_work("灯火阑珊处，武汉夜色美", "我在武汉游玩了一天，去了武汉国际广场、欣赏了城市夜景。请写一段轻松明快的游记", image_descriptions)
    # print(outline_result)
    # # print(outline_result['data']['content'])
    #
    # cleaned_text = outline_result['data']['content'].strip("```json").strip("```").strip()
    # print(cleaned_text)
    # # 将清理后的文本解析为 JSON 对象
    # try:
    #     json_data = json.loads(cleaned_text)
    # except json.JSONDecodeError as e:
    #     print(f"JSON 解码失败: {e}")
    #     exit()
    #
    #     # 保存为 JSON 文件
    # output_file = "travel_outline_json.json"
    # with open(output_file, "w", encoding="utf-8") as f:
    #     json.dump(json_data, f, ensure_ascii=False, indent=4)
    #
    # print(f"JSON 文件已成功保存为 {output_file}！")
    #
    # # #
    # theme = "灯火阑珊处，武汉夜色美"
    # travel_descriptions = "我在武汉游玩了一天，去了武汉国际广场、欣赏了城市夜景，品尝了热干面。请写一段轻松明快的游记"
    # outline = generate_travel_frame_work(theme=theme, travel_descriptions=travel_descriptions, image_descriptions=image_descriptions)['data']['content']
    # # 调用函数
    # result = generate_travel_notes(theme=theme, outline=outline, image_descriptions=image_descriptions)
    # # #
    # # 打印结果
    # if result["status"]:
    #     print("游记生成成功！")
    #     print("\n标题:", result["data"]["title"])
    #     print("\n大纲:")
    #     for item in result["data"]["outline"]:
    #         print(f"- {item}")
    #     print("\n正文:")
    #     print(result["data"]["content"])
    #     print("\n使用的图片:")
    #     for img_url in result["data"]["images"]:
    #         print(f"- {img_url}")
    # else:
    #     print("生成失败:", result["data"])

    # 示例数据
    # theme = "城市与童趣的邂逅"
    # outline = [
    #     "都市之美",
    #     "璀璨夜景",
    #     "童趣时光",
    #     "生活的诗意"
    # ]

    # 调用函数
    # result = generate_travel_notes(theme, outline, image_descriptions)

    # # 打印结果
    # if result["status"]:
    #     print("游记生成成功！")
    #     print("\n标题:", result["data"]["title"])
    #     print("\n大纲:")
    #     for i, item in enumerate(result["data"]["outline"], 1):
    #         print(f"{i}. {item}")
    #     print("\n正文:")
    #     print(result["data"]["content"])
    #     print("\n使用的图片:")
    #     for img_url in result["data"]["images"]:
    #         print(f"- {img_url}")
    # else:
    #     print("生成失败:", result["data"])

    # # 打印结果
    # if result["status"]:
    #     print("游记生成成功！")
    #     print("\n标题:", result["data"]["title"])
    #     print("###############################")
    #     print("\n大纲:")
    #     # for item in result["data"]["outline"]:
    #     #     print(f"- {item}")
    #     print(result["data"]["outline"])
    #     print("###############################")
    #     print("\n正文:")
    #     print(result["data"]["content"])
    #     print("###############################")
    #     print("\n网络图片:")
    #     for url in result["data"]["images"]["network"]:
    #         print(f"- {url}")
    #
    #     print("\n本地图片:")
    #     for path in result["data"]["images"]["local"]:
    #         print(f"- {path}")
    #
    #     print("\n图片描述:")
    #     for desc in result["data"]["descriptions"]:
    #         print(f"- 路径: {desc['path']}")
    #         print(f"  描述: {desc['description']}")
    #         print(f"  类型: {'网络图片' if desc['is_url'] else '本地图片'}")
    #         print()
    # else:
    #     print("生成失败:", result["data"])
    #
    #
    # generate_markdown_article(result, output_path="travel_notes_005_006xiaohongshu.md")
    md2json(r"E:\mp-writer-agent\src\api\backend\self_media\travel_notes.md")