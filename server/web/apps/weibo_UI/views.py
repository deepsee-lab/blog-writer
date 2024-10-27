# -*- coding: utf-8 -*-
# Standard library imports.
import sqlite3,os,json,re,requests,uuid,urllib.request,datetime,pyperclip
# Related third party imports.
from flask import Flask, Blueprint,render_template,request,jsonify,url_for,current_app,session,redirect,g
from flask_cors import CORS, cross_origin
from functools import wraps
from loguru import logger
from werkzeug.utils import secure_filename
from extends import (
    db,
)
# Local application/library specific imports.
from apps.weibo_UI.rag_run import *
from apps.weibo_UI.models import weibo_Model_setting,weibo_Pic_add_Model,weibo_wpp_add_draft_Model
bp = Blueprint("weibo_UI", __name__, url_prefix='/weibo_UI',static_folder='static',template_folder='templates')

verify_code=0
##############################################################################################
#  网页功能部分
##############################################################################################

############################################
#vue3
@bp.route('/api/v1/login/code',methods=['GET'] )
def login_code():
    data_dict={}
    data_dict['code']=0
    data_dict['data']="http://dummyimage.com/100x40/dcdfe6/000000.png&text=WeiBoAI"
    data_dict['message']="获取验证码成功"
    return data_dict

@bp.route('/api/v1/users/login',methods=['GET','POST'] )
def users_login():
    if request.method == "POST":
        code = request.json['code']
        username = request.json['username']
        password = request.json['password']
        print('123',username)
        if code =="WeiBoAI" and username=='admin' and password=='12345678':
            result={
                "code":0,
                "data":{
                    "token":"taken-admin"
                },
                "message":"登录成功"
            }
        else:
            result={
                "code":400,
                "message":"登录失败"
            }
    return result

@bp.route('/api/v1/users/info',methods=['GET','POST'] )
def user_info():
    if request.method == "GET":
        result={
            "code":0,
            "data":{
                "username":"admin",
                "roles":["admin"]
            },
            "message":"获取用户详情成功"
        }
    return result
#######################################
#KB  
##KB 对话 
###vue3
@bp.route('/api/v1/KB/list',methods=['GET'] )
def kb_list_all():
    try:
        result=kb_list()
        #print('-----')
        result['code']=0
    except:
        result={}
        result['code']=400
    return result

@bp.route('/api/v1/model/result',methods=['GET','POST'] )
def result_KB():
    if request.method == "POST":
        type_name=request.json['Type_item']
        model_select=request.json['Model_item']
        KB_id=request.json['KB_item']
        top_K=request.json['Top_K']
        Temprature=request.json['Temprature']
        query=request.json['Query_content']
        retrieve_result=request.json['KB_result']
        rag_result=request.json['answer_content']
        url = 'http://127.0.0.1:7020/inference'
        # 检查响应状态代码
        logger.info('rag_before:',KB_id)
        logger.info(KB_id)
        answer=vector_model_rag(url,KB_id,top_K,query,type_name,model_select)
        if answer['message'] == 'success':
            # 打印响应文本
            rag_result=answer['data']['rag_result']
            retrieve_result=answer['data']['retrieve_result'][0][0]['entity']['text']
        result={
            "code":0,
            "data":{
                "Type_item":type_name,
                "Model_item":model_select,
                "KB_item":KB_id,
                "Top_K":top_K,
                "Temprature":Temprature,
                "Query_content":query,
                "KB_result":retrieve_result,
                "answer_content":rag_result
            },
            "message":"获取知识库答案详情成功"
        }
        print('find answer')
        print(retrieve_result)
    return result

@bp.route('/api/v1/model/type',methods=['GET','POST'] )
def type_list_all():
    if request.method == "GET":
        type_list=[]
        model_dict={}
        try:
            res=os.popen("ps -ef | grep ollama").read()
            if 'ollama serve' in res:
                model_dict={}
                model_dict['type']='ollama'
                type_list.append(model_dict)
        except:
            logger.info('no ollama')
        try:
            res=os.popen("ps -ef | grep xinference").read()
            if 'xinference' in res:
                model_dict={}
                model_dict['type']='xinference'
                type_list.append(model_dict)
        except:
            logger.info('no xinference')
        choose_dict={}
        choose_dict['code']=0
        choose_dict['type_list']=type_list
        print('type list:',type_list)
    return choose_dict

@bp.route('/api/v1/model/list',methods=['GET','POST'] )
def model_list_all():
    result={}
    if request.method == "POST":
        model_list=[]
        type_select = request.json['Type_item']
        print('123',type_select)
        if "ollama" in type_select:
            try:
                res=os.popen("ollama list").read()
                models=res.split('\n')
                for index_i, item_i in enumerate(models):
                    model_dict={}
                    if index_i == 0:
                        continue
                    model_dict['name']=item_i.split()[0]
                    model_list.append(model_dict)
                    print(item_i.split()[0])
            except:
                #print('nono no')
                logger.info('no ollama')
        result['code']=verify_code
        result['data']=model_list
    return result

@bp.route('/api/v1/model/setting',methods=['GET','POST'] )
def mode_setting():
    if request.method == "POST":
        type_name=request.json['Type_item']
        model_select=request.json['Model_item']
        top_K=request.json['Top_K']
        Temprature=request.json['Temprature']
        max_time=request.json['max_time']
        file_model=weibo_Model_setting()
        file_model.Type_item      = type_name
        file_model.Model_item     = model_select
        file_model.Temprature     = Temprature
        file_model.Top_K          = top_K
        file_model.max_time       = max_time
        db.session.add(file_model)
        db.session.commit()
        # 检查响应状态代码
        result={
            "code":0,
            "data":{
                "Type_item":type_name,
                "Model_item":model_select,
                "Top_K":top_K,
                "Temprature":Temprature,
                "max_time":max_time
            },
            "message":"配置成功"
        }
        print('find answer')
    return result

#######################################
#KB  0000+++++++++++++++
##KB 建立
###vue3
@bp.route('/api/v1/Vector/list',methods=['GET'] )
def vector_list_all():
    result={}
    vector_list=[]
    ##########
    vector_dict={}
    vector_dict['name']='milvus'
    vector_list.append(vector_dict)
    ##########
    result['code']=verify_code
    result['data']=vector_list
    result['message']="获取向量数据库详情成功"
    return result

@bp.route('/api/v1/Embedding/list',methods=['GET'] )
def embedding_list_all():
    result={}
    embedding_list=[]
    ##########
    embedding_dict={}
    embedding_dict['name']='bge-large-zh-v1.5'
    embedding_list.append(embedding_dict)
    ##########
    result['code']=verify_code
    result['data']=embedding_list
    result['message']="获取embedding模型详情成功"
    return result

@bp.route('/api/v1/KB/upload',methods=['GET','POST'] )
@cross_origin()
def KB_upload_file():
    if request.method == "POST":
        result={}
        if 'file' not in request.files:
            message='No file part'
            status=400
        file = request.files['file']
        if file.filename == '':
            message='No selected file'
            status= 400
        if file:
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename))
            message='File uploaded successfully'
            status=200
        result['message']=message
        result['status']=status
        result['code']=verify_code
        return result


@bp.route('/api/v1/Embedding/create',methods=["POST","GET"])
def submit_kb():
    if request.method == "POST":
        result={}
        unique_id=str(uuid.uuid4()).replace('-','')
        # 02d2f68d6de441c38968c6b58b31dcfd
        unique_id='kb'+unique_id[2:]
        Kb_name = request.json['KB_name']
        desc = request.json['desc']
        Dim=1024
        Kb_id=unique_id
        vector_store_name = request.json['vector_name']
        embedding_model_name = request.json['embedding_model_name']
        url = 'http://127.0.0.1:6020/vector/kb_add_one'
        json_data = {
          "kb_id": Kb_id,
          "kb_name": Kb_name,
          "kb_desc": desc,
          "vector_store_name": vector_store_name,
          "embedding_model_name": embedding_model_name,
          "dim": Dim
        }
        # 发送请求并存储响应
        response = requests.post(url, json=json_data)
        #print(response.json())
        # 检查响应状态代码
        answer=response.json()
        message='创建失败'
        if answer['success']:
            message='创建成功'
        result['message']=message
        result['code']=verify_code
        return result

@bp.route('/api/v1/Embedding/doc_list',methods=["POST","GET"])
def list_file_doc():
    if request.method == "GET":
        filepath=current_app.config['UPLOAD_FOLDER']
        files=os.listdir(filepath)
        File_lists = []
        result={}
        ##########
        for file in files:
            file_dict={}
            file_dict['name']=file
            File_lists.append(file_dict)
        ##########
        result['code']=verify_code
        result['data']=File_lists
        result['message']="获取文件详情成功"
        return result

@bp.route('/api/v1/Embedding/doc_base',methods=["POST","GET"])
def doc_base_list():
    if request.method == "GET":
        result={}
        base_list=[]
        ##########
        base_dict={}
        base_dict['name']='doc_content_base64'
        base_list.append(base_dict)
        ##########
        result['code']=verify_code
        result['data']=base_list
        result['message']="获取doc base详情成功"
        return result
    
@bp.route('/api/v1/Embedding/create_doc',methods=["POST","GET"])
def doc_create():
    if request.method == "POST":
        result={}
        kb_id = request.json['kb_id']
        doc_id = request.json['doc_id']
        doc_name = request.json['doc_name']
        doc_path = request.json['doc_path']
        doc_content = request.json['doc_content']
        filepath=os.path.join(current_app.config['UPLOAD_FOLDER'], doc_path)
        url = 'http://127.0.0.1:6020/vector/doc_add_one'
        json_data = {
            "kb_id": kb_id,
            "doc_id": doc_id,
            "doc_name": doc_name,
            "doc_path": filepath,
            "doc_content_base64": doc_content
        }
        # 发送请求并存储响应
        response = requests.post(url, json=json_data)
        #print(response.json())
        # 检查响应状态代码
        answer=response.json()
        message='创建失败'
        if answer['success']:
            message='创建成功'
        result['message']=message
        result['code']=verify_code
        return result
#############################################
#######################################
#wei xin
##素材 建立
###vue3 
@bp.route('/api/v1/Wenxin/update_token',methods=['GET','POST'] )
def Wenxin_update_token():
    if request.method == "POST":
        result={}
        appid=os.getenv('appid')
        secret=os.getenv('secret')
        ####  post  ####
        url_self_media= 'http://127.0.0.1:6050/wpp/stable_access_token_get'
        json_data_self_media = {
            "appid": appid,
            "secret": secret
        }
        # 发送请求并存储响应
        response_self_media = requests.post(url_self_media, json=json_data_self_media)
        self_media_res=response_self_media.json()
        token_status='get token fail'
        content=token_status
        message=token_status
        status=400
        if self_media_res['success']:
            content=self_media_res['data']['stable_access_token']['access_token']
            file_path =current_app.config['VAR_FILE_PATH']
            new_line=[]
            with open(file_path, 'r') as file:
                lines = file.readlines()
                for item in lines:
                    if 'access_token=' in item:
                        str_line='access_token='+content
                        new_line.append(str_line)
                    else:
                        new_line.append(item)
            # 将修改后的内容写回文件
            with open(file_path, 'w') as file:
                file.writelines(new_line)
            message='更新成功'
            status=200
        result['content']=content  
        result['message']=message
        result['status']=status
        result['code']=verify_code
        return result
    
@bp.route('/api/v1/Wenxin/upload',methods=['GET','POST'] )
@cross_origin()
def Wenxin_upload_file():
    if request.method == "POST":
        result={}
        if 'file' not in request.files:
            message='No file part'
            status=400
        file = request.files['file']
        if file.filename == '':
            message='No selected file'
            status= 400
        if file:
            pic_path=os.path.join(current_app.config['UPLOAD_FOLDER_PIC'], file.filename)
            file.save(pic_path)
            access_token=os.getenv('access_token')
            logger.info(pic_path)
            logger.info(access_token)
            ####  post  ####
            url_self_media= 'http://127.0.0.1:6050/wpp/material_img_add'
            json_data_self_media = {
                "access_token": access_token,
                "file_path": pic_path
            }
            print(pic_path)
            print(access_token)
            # 发送请求并存储响应
            response_self_media = requests.post(url_self_media, json=json_data_self_media)
            self_media_res=response_self_media.json()
            message='wpp fail'
            if self_media_res['success']:
                #print('hjhhhh')
                new_picture = weibo_Pic_add_Model()
                new_picture.name     = file.filename
                new_picture.media_id = self_media_res['data']['media_id']
                new_picture.url      = self_media_res['data']['url']
                db.session.add(new_picture)
                db.session.commit()
                message='File uploaded successfully'
                status=200
        result['message']=message
        result['status']=status
        result['code']=verify_code
        return result

@bp.route('/api/v1/Wenxin/txt_to_pic',methods=["POST","GET"])
def WX_txt_to_pic():
    if request.method == "POST":
        result={}
        text = request.json['Data']
        print(text)
        url_self_media= 'https://83440n0z70.vicp.fun/image/FLUX_1_dev/generate'
        json_data_picture = {
            "prompt": text,
            "filename": "demo",
            "upload_to_cdn": True,
            "bucket_name": "wwa-test",
            "expire_time": 3600
        }
        response_self_media = requests.post(url_self_media, json=json_data_picture)
        logger.info(response_self_media.text)
        self_media_res=response_self_media.json()
        result['success']=False
        message='文生图失败'
        if self_media_res['success']:
            url_link=self_media_res['data']['url']
            logger.info(url_link)
            #url_link="http://sicmnykdc.hd-bkt.clouddn.com/png/257d42325be94c7fada905650e5d0fac.png"
            tiem_str=str(datetime.datetime.today())
            file_pic=text+'_'+tiem_str+'.png'
            file_pic=file_pic.replace(' ','_').replace(':','').replace('-','')
            file_path_pic=os.path.join(current_app.config['UPLOAD_FOLDER_PIC'], file_pic)
            urllib.request.urlretrieve(url_link, file_path_pic)
            message='文生图成功'
            result['Data']=url_link
        result['message']=message
        result['code']=verify_code
        return result

#######################################
#wei xin
##草稿 建立
###vue3 
@bp.route('/api/v1/Wenxin/acticle_type',methods=['GET','POST'] )
def acticle_type():
    result={}
    if request.method == "GET":
        type_list=[]
        data_list=['旅游攻略','知识分享','热点新闻','其他']
        try:
            for index_i, item_i in enumerate(data_list):
                data_dict={}
                data_dict['name']=item_i
                type_list.append(data_dict)
        except:
            #print('nono no')
            logger.info('add fail')
        result['code']=verify_code
        result['data']=type_list
    return result

@bp.route('/api/v1/Wenxin/acticle_style',methods=['GET','POST'] )
def acticle_style():
    result={}
    if request.method == "GET":
        type_list=[]
        data_list=['客观陈述风格','叙述性风格','抒情风格','描写性风格','现实风格','无特别要求']
        try:
            for index_i, item_i in enumerate(data_list):
                data_dict={}
                data_dict['name']=item_i
                type_list.append(data_dict)
        except:
            #print('nono no')
            logger.info('add fail')
        result['code']=verify_code
        result['data']=type_list
    return result

@bp.route('/api/v1/Wenxin/word_number',methods=['GET','POST'] )
def acticle_word_number():
    result={}
    if request.method == "GET":
        type_list=[]
        data_list=['100~300','300~400','400~500','500~600','600~700','700~900']
        try:
            for index_i, item_i in enumerate(data_list):
                data_dict={}
                data_dict['name']=item_i
                type_list.append(data_dict)
        except:
            #print('nono no')
            logger.info('add fail')
        result['code']=verify_code
        result['data']=type_list
    return result

@bp.route('/api/v1/Wenxin/word_style',methods=['GET','POST'] )
def word_style():
    result={}
    if request.method == "GET":
        type_list=[]
        data_list=['生动形象','诙谐幽默','通俗明快','朴素自然','悲壮慷慨','豪迈雄奇','徇丽飘逸','悲壮慷慨','沉郁顿挫','婉约细腻','无特别要求']
        try:
            for index_i, item_i in enumerate(data_list):
                data_dict={}
                data_dict['name']=item_i
                type_list.append(data_dict)
        except:
            #print('nono no')
            logger.info('add fail')
        result['code']=verify_code
        result['data']=type_list
    return result

@bp.route('/api/v1/Wenxin/create_draft',methods=["POST","GET"])
def WX_create_draft():
    if request.method == "POST":
        result={}
        ####
        Type_item = request.json['Type_item']
        Title_item = request.json['Title_item']
        Content_item = request.json['Content_item']
        Style_item = request.json['Style_item']
        Word_number = request.json['Word_number']
        Word_style = request.json['Word_style']
        base_prompt = """
        帮我写一篇`{}`公众号文章，要求如下：
        文章题目：`{}`
        文章整体风格：`{}`
        文章字数在:`{}`
        语言风格突出`{}`，吸引读者关注。
        """.strip()
        prompt = base_prompt.format('\n'.join(Content_item), Type_item,Title_item,Style_item,Word_number,Word_style)
        url = 'http://127.0.0.1:4010/private/inference'
        # 检查响应状态代码
        answer=no_vector_model_rag(url,prompt)
        res_result=''
        if answer['message'] == 'success':
            # 打印响应文本
            res_result=answer['data']['result']
            result={
                "code":verify_code,
                "data":{
                    "Type_item":Type_item,
                    "Title_item":Title_item,
                    "Content_item":Content_item,
                    "Style_item":Style_item,
                    "Word_number":Word_number,
                    "Word_style":Word_style,
                    "Result_item":res_result
                },
                "message":"获取成功"
            }
        return result

@bp.route('/api/v1/Wenxin/content_prompt',methods=["POST","GET"])
def WX_content_prompt():
    if request.method == "POST":
        result={}
        ####
        Type_item = request.json['Type_item']
        Title_item = request.json['Title_item']
        Content_item = request.json['Content_item']
        Style_item = request.json['Style_item']
        Word_number = request.json['Word_number']
        Word_style = request.json['Word_style']
        base_prompt = """
        我想写一篇`{}`公众号文章，要求如下：
        文章题目：`{}`
        文章整体风格：`{}`
        文章字数在:`{}`
        语言风格突出`{}`，吸引读者关注。
        我的要写的内容提示为`{}`，请帮我优化一下内容提示，让它更清晰一些
        """.strip()
        prompt = base_prompt.format(Type_item,Title_item,Style_item,Word_number,Word_style,Content_item)
        url = 'http://127.0.0.1:4010/private/inference'
        # 检查响应状态代码
        answer=no_vector_model_rag(url,prompt)
        print('--------',str(answer))
        res_result=''
        if answer['message'] == 'success':
            # 打印响应文本
            res_result=answer['data']['result']
            result={
                "code":verify_code,
                "data":{
                    "Type_item":Type_item,
                    "Title_item":Title_item,
                    "Content_item":Content_item,
                    "Style_item":Style_item,
                    "Word_number":Word_number,
                    "Word_style":Word_style,
                    "Result_item":res_result,
                    "code":0
                },
                "message":"获取成功"
            }
        return result
#######################################
#wei xin
##发布 建立
###vue3 
@bp.route('/api/v1/Wenxin/thumb_media_data',methods=['GET','POST'] )
def thumb_media_data():
    result={}
    if request.method == "GET":
        item_list = weibo_Pic_add_Model.query.all()
        Pic_lists = []
        for item in item_list:
            temp_dict={}
            temp_dict['name']=item.name
            temp_dict['url']=item.url
            temp_dict['thumb_media_id']=item.media_id
            Pic_lists.append(temp_dict)
        result['data']=Pic_lists
        result['code']=verify_code
    return result

@bp.route('/api/v1/Wenxin/need_open_data',methods=['GET','POST'] )
def need_open_data():
    result={}
    if request.method == "GET":
        type_list=[]
        data_list=['open','close']
        try:
            for index_i, item_i in enumerate(data_list):
                data_dict={}
                data_dict['name']=item_i
                type_list.append(data_dict)
        except:
            #print('nono no')
            logger.info('add fail')
        result['code']=verify_code
        result['data']=type_list
    return result

@bp.route('/api/v1/Wenxin/fans_comment',methods=['GET','POST'] )
def fans_comment():
    result={}
    if request.method == "GET":
        type_list=[]
        data_list=['open','close']
        try:
            for index_i, item_i in enumerate(data_list):
                data_dict={}
                data_dict['name']=item_i
                type_list.append(data_dict)
        except:
            #print('nono no')
            logger.info('add fail')
        result['code']=verify_code
        result['data']=type_list
    return result

@bp.route('/api/v1/Wenxin/WX_submit_draft',methods=["POST","GET"])
def WX_submit_draft():
    if request.method == "POST":
        result={}
        ####
        access_token=os.getenv('access_token')
        author = request.json['author']
        Title_item = request.json['Title_item']
        digest = request.json['digest']
        content = request.json['content']
        content_source_url = request.json['content_source_url']
        thumb_media_id = request.json['thumb_media_id']
        need_open_comment = request.json['need_open_comment']
        only_fans_can_comment = request.json['only_fans_can_comment']
        if 'open' in need_open_comment:
            need_open_comment_num=1
        else:
            need_open_comment_num=0
        if 'open' in only_fans_can_comment:
            only_fans_can_comment_num=1
        else:
            only_fans_can_comment_num=0
        ####  post  ####
        print('access_token',access_token)
        print('thumb_media_id',thumb_media_id)
        url_self_media= 'http://127.0.0.1:6050/wpp/draft_add'
        json_data_self_media = {
            "access_token": access_token,
            "title": Title_item,
            "author": author,
            "digest": digest,
            "content": content,
            "content_source_url": content_source_url,
            "thumb_media_id": thumb_media_id,
            "need_open_comment": need_open_comment_num,
            "only_fans_can_comment": only_fans_can_comment_num
        }
        response_self_media = requests.post(url_self_media, json=json_data_self_media)
        self_media_res=response_self_media.json()
        message='添加失败'
        if self_media_res['success']:
            message="成功添加"
            new_wpp_draft = weibo_wpp_add_draft_Model()
            new_wpp_draft.title               = re.sub('[^\u4e00-\u9fa5]+','',Title_item) #去除不可见字符
            new_wpp_draft.user                = author
            new_wpp_draft.thumb_media_id      = thumb_media_id
            new_wpp_draft.media_id            = self_media_res['data']['media_id']
            new_wpp_draft.digest              = re.sub('[^\u4e00-\u9fa5]+','',digest) #去除不可见字符
            new_wpp_draft.content             = re.sub('[^\u4e00-\u9fa5]+','',content) #去除不可见字符
            new_wpp_draft.content_source_url  = content_source_url
            db.session.add(new_wpp_draft)
            db.session.commit()
        result['success']=self_media_res['success']
        result['code']=verify_code
        result['data']=message
        return result

@bp.route('/api/v1/Wenxin/MEDIA_ID_list',methods=['GET','POST'] )
def MEDIA_ID_list():
    result={}
    if request.method == "GET":
        type_list=[]
        media_id_list = weibo_wpp_add_draft_Model.query.all()
        for item_one in media_id_list:
            data_dict={}
            data_dict['value']=item_one.media_id
            data_dict['name']=item_one.title
            type_list.append(data_dict)
        result['code']=verify_code
        result['data']=type_list
    return result

@bp.route('/api/v1/Wenxin/WX_publish_draft',methods=['GET','POST'] )
def WX_publish_draft():
    result={}
    if request.method == "POST":
        access_token=os.getenv('access_token')
        MEDIA_ID = request.json['MEDIA_ID']
        url_self_media= 'http://127.0.0.1:6050/wpp/publish_free'
        json_data_self_media = {
            "access_token": access_token,
            "MEDIA_ID": MEDIA_ID
        }
        # 发送请求并存储响应
        response_self_media = requests.post(url_self_media, json=json_data_self_media)
        self_media_res=response_self_media.json()
        message='发布失败'
        if self_media_res['success']:
            message='发布成功'
        result['success']=self_media_res['success']
        result['code']=verify_code
        result['data']=message
    return result

#######################################
#Dashboard
##prompt 建立
###vue3 
@bp.route('/api/v1/Dashboard/chat',methods=['GET','POST'] )
def Dashboard_chat():
    result={}
    if request.method == "POST":
        Content_item = request.json['Content_item']
        prompt = Content_item
        url = 'http://127.0.0.1:4010/private/inference'
        # 检查响应状态代码
        answer=no_vector_model_rag(url,prompt)
        print('--------',str(answer))
        res_result=''
        if answer['message'] == 'success':
            # 打印响应文本
            res_result=answer['data']['result']
            result={
                "code":verify_code,
                "data":{
                    "Content_item":Content_item,
                    "Result":res_result,
                    "code":0
                },
                "message":"获取成功"
            }
        return result