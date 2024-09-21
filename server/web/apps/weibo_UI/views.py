# -*- coding: utf-8 -*-
# Standard library imports.
import sqlite3,os,json,re,requests,uuid,urllib.request,datetime,pyperclip
# Related third party imports.
from flask import Flask, Blueprint,render_template,request,jsonify,url_for,current_app,session,redirect,g
from functools import wraps
from loguru import logger
from werkzeug.utils import secure_filename
from extends import (
    db,
)
# Local application/library specific imports.
from apps.weibo_UI.rag_run import *
from apps.weibo_UI.models import weibo_UI_Model,weibo_Pic_Model,weibo_Vedio_Model,weibo_wpp_add_draft_Model,weibo_file_change_Model

bp = Blueprint("weibo_UI", __name__, url_prefix='/weibo_UI',static_folder='static',template_folder='templates')


##############################################################################################
#  网页功能部分
##############################################################################################

@bp.before_request
def before_request():
    if session.get('name'):
        result = weibo_UI_Model.query.filter_by(name=session.get('name')).first()
        if result:
            g.user = session.get('name')
        else:
            g.user = None
    else:
        g.user = None

def login_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if g.user:
            result = weibo_UI_Model.query.filter_by(name=g.user).first()
            if result:
                return func(*args, **kwargs)
            else:
                return redirect('/weibo_UI/login')
        else:
            return redirect('/weibo_UI/login')
    return inner


@bp.route('/index' )
@login_required
def show():
    username=session.get("name")
    print('qwe',username)
    return render_template('index.html',username=username)

@bp.route('/login',methods=['GET','POST'] )
def login():
    if request.method == 'GET':
        return render_template('pages_login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        users = weibo_UI_Model.query.all()
        gate_key=0
        for user in users:
            if user.name==username and user.text==password:
                gate_key=1
                session["name"] = username
                session["pwd"] = password
                return render_template('index.html',username=username)

@bp.route('/logout',methods=['GET','POST'] )
@login_required
def logout():
    session.clear()
    return render_template('pages_login.html')

@bp.route('/add_user',methods=['GET','POST'] )
def add_user():
    if request.method == "POST":
        data = request.get_json()
        UserName=data['UserName']
        Pwd=data['Pwd']
        new_user = weibo_UI_Model()
        new_user.name = UserName
        new_user.text = Pwd
        db.session.add(new_user)
        db.session.commit()
        choose_dict={}
        choose_dict['result']=1
        return jsonify(choose_dict)
    return render_template('add_user.html')


@bp.route('/get_by_id',methods=['GET','POST'] )
@login_required  
def get_by_id():
    get_user = weibo_UI_Model.query.get(1)  # User.query.filter_by(id=get_id).first()
    return "编号：{0}，用戶名：{1}，邮箱：{2}".format(get_user.id, get_user.name, get_user.text)

##########################################################################################################


@bp.route('/submit_file_parsing',methods=["POST","GET"])
@login_required  
def submit_file_parsing():
    if request.method == "POST":
        data = request.get_json()
        if 'selec_file' in data['Type']:
            filepath=current_app.config['UPLOAD_FOLDER']
            files=os.listdir(filepath)
            file_dict={}
            file_dict['list']=files
            return jsonify(file_dict)
        elif 'add_file_parsing' in data['Type']:
            #'doc_id_parsing':doc_id_parsing,'doc_name_parsing':doc_name_parsing,'doc_file_parsing':doc_file_parsing,'doc_file_parsing_way':doc_file_parsing_way}
            doc_id_parsing=data['doc_id_parsing']
            doc_name_parsing=data['doc_name_parsing']
            doc_file_parsing=data['doc_file_parsing']
            doc_file_parsing_way=data['doc_file_parsing_way']
            filepath=os.path.join(current_app.config['UPLOAD_FOLDER'], doc_file_parsing)
            if 'doc_to_json' in doc_file_parsing_way:
                url = 'http://127.0.0.1:7030/document/docx_to_json'
            elif 'doc_to_text' in doc_file_parsing_way:
                url = 'http://127.0.0.1:6020/vector/doc_add_one'
            json_data = {
                    "doc_id": doc_id_parsing,
                    "doc_name": doc_name_parsing,
                    "doc_path": filepath
            }
            # 发送请求并存储响应
            response = requests.post(url, json=json_data)
            #print(response.json())
            # 检查响应状态代码
            res=''
            answer=response.json()
            choose_dict={}
            choose_dict['result']=0
            if answer['success']:
                choose_dict['result']=1
            return jsonify(choose_dict)
    username=session.get("name")
    return render_template('upload_Document.html',username=username,status='')


######################################################################################
# 知识库
######################################################################################
@bp.route('/choose_model')
@login_required  
def choose_model():
    username=session.get("name")
    return render_template('choose_model.html',username=username)
#################################################################
############     1、 知识库问答
#################################################################
@bp.route('/choose_model_post',methods=["POST"])
@login_required  
def choose_model_post():
    if request.method == "POST":
        data = request.get_json()
        type_name=data['type_name']
        model_type=['-- pls choose --']
        kb_list_content=[]
        if "choose_type" in type_name:
            try:
                res=os.popen("ps -ef | grep ollama").read()
                if 'ollama serve' in res:
                    model_type.append("ollama")
            except:
                logger.info('no ollama')
            try:
                res=os.popen("ps -ef | grep xinference").read()
                if 'xinference' in res:
                    model_type.append("xinference")
            except:
                logger.info('no xinference')
            choose_dict={}
            choose_dict['result']=1
            choose_dict['content']=model_type
            return jsonify(choose_dict)
        elif "choose_model" in type_name:
            type_select=data['type_select']
            model_list=[]
            if "ollama" in type_select:
                try:
                    res=os.popen("ollama list").read()
                    models=res.split('\n')
                    for index_i, item_i in enumerate(models):
                        if index_i == 0:
                            continue
                        model_list.append(item_i.split()[0])
                        print(item_i.split()[0])
                except:
                    logger.info('no ollama')
            choose_dict={}
            choose_dict['result']=1
            choose_dict['content']=model_list
            return jsonify(choose_dict)
        elif "choose_KB" in type_name:
            try:
                res=kb_list()
                kb_list_content=res['data']['kb_list']
                logger.info('kb_list')
                
            except:
                logger.info('no get kb list')
            choose_dict={}
            choose_dict['result']=1
            choose_dict['content']=kb_list_content
            logger.info(kb_list_content)
            return jsonify(choose_dict)

@bp.route('/model_run',methods=["POST"])
@login_required  
def model_run():
    if request.method == "POST":
        data = request.get_json()
        type_name=data['type_name']
        model_select=data['model_name']
        KB_id=data['KB_id']
        top_selector=data['top_selector']
        top_K=int(top_selector)
        query=data['query']
        logger.info(KB_id)
        logger.info(query)
        if KB_id=='0':
            url = 'http://127.0.0.1:4010/private/inference'
            # 检查响应状态代码
            rag_result=''
            retrieve_result=''
            answer=no_vector_model_rag(url,query,type_name,model_select)
            if answer['message'] == 'success':
                # 打印响应文本
                rag_result=answer['data']['result']
                retrieve_result='(no select vector)'
        else:
            url = 'http://127.0.0.1:7020/inference'
            # 检查响应状态代码
            rag_result=''
            retrieve_result=''
            logger.info('rag_before:',KB_id)
            logger.info(KB_id)
            answer=vector_model_rag(url,KB_id,top_K,query,type_name,model_select)
            if answer['message'] == 'success':
                # 打印响应文本
                rag_result=answer['data']['rag_result']
                retrieve_result=answer['data']['retrieve_result'][0][0]['entity']['text']
        choose_dict={}
        choose_dict['result']=1
        choose_dict['rag_result']=rag_result
        choose_dict['retrieve_result']=retrieve_result
        #choose_dict['content']=response
        return jsonify(choose_dict)
#################################################################
############     2、 新建知识库
#################################################################
@bp.route('/upload',methods=['GET','POST'])
@login_required  
def upload():
    username=session.get("name")
    status=''
    if request.method == "POST":
        f = request.files['file']
        unique_id=str(uuid.uuid4()).replace('-','')[10:]
        filename=unique_id+'.docx'
        filename=secure_filename(filename)
        save_path=os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        print(save_path)
        if not os.path.exists(current_app.config['UPLOAD_FOLDER']):
            os.mkdir(current_app.config['UPLOAD_FOLDER'])
        f.save(save_path)
        status="upload ok"
        f=str(f.filename).replace('《','').replace('》','').replace('-','').replace('=','').replace('。','').replace(':','')
        file_model=weibo_file_change_Model()
        file_model.initial_filename     = f
        file_model.temp_filename        = filename
        db.session.add(file_model)
        db.session.commit()
    return render_template('upload_Document.html',username=username,status=status)

@bp.route('/submit_kb',methods=["POST","GET"])
@login_required  
def submit_kb():
    if request.method == "POST":
        unique_id=str(uuid.uuid4()).replace('-','')
        #print('lll',unique_id)
        # 02d2f68d6de441c38968c6b58b31dcfd
        unique_id='kb'+unique_id[2:]
        data = request.get_json()
        Dim=1024
        Kb_id=unique_id
        Kb_name=data['Kb_name']
        desc=data['desc']
        vector_store_name=data['vector_store_name']
        embedding_model_name=data['embedding_model_name']
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
        res=''
        answer=response.json()
        choose_dict={}
        choose_dict['result']=0
        if answer['success']:
            choose_dict['result']=1
        #choose_dict['content']=res
        #choose_dict['content']=response
        return jsonify(choose_dict)
    username=session.get("name")
    return render_template('upload_Document.html',username=username,status='')

@bp.route('/submit_doc',methods=["POST","GET"])
@login_required  
def submit_doc():
    if request.method == "POST":
        data = request.get_json()
        if 'selec_file' in data['Type']:
            #filepath=current_app.config['UPLOAD_FOLDER']
            #files=os.listdir(filepath)
            item_list=weibo_file_change_Model.query.all()
            File_lists = []
            choose_dict={}
            for item in item_list:
                temp_dict={}
                temp_dict['old']=item.initial_filename
                print('++++',item.initial_filename)
                temp_dict['new']=item.temp_filename
                File_lists.append(temp_dict)
            choose_dict['content']=File_lists
            return jsonify(choose_dict)
        elif 'add_doc' in data['Type']:
            Kb_id_doc=data['Kb_id_doc']
            print('222',Kb_id_doc)
            Doc_id=data['Doc_id']
            Doc_name=data['Doc_name']
            doc_file=data['doc_file']
            filepath=os.path.join(current_app.config['UPLOAD_FOLDER'], doc_file)
            doc_content_base64=data['doc_content_base64']
            url = 'http://127.0.0.1:6020/vector/doc_add_one'
            json_data = {
                "kb_id": Kb_id_doc,
                "doc_id": Doc_id,
                "doc_name": Doc_name,
                "doc_path": filepath,
                "doc_content_base64": doc_content_base64
            }
            # 发送请求并存储响应
            response = requests.post(url, json=json_data)
            #print(response.json())
            # 检查响应状态代码
            res=''
            answer=response.json()
            choose_dict={}
            choose_dict['result']=0
            if answer['success']:
                choose_dict['result']=1
            return jsonify(choose_dict)
    username=session.get("name")
    return render_template('upload_Document.html',username=username,status='')

######################################################################################
# 微信公众号
######################################################################################

#################################################################
############     1、 上传素材
#################################################################
@bp.route('/text_to_picture_video',methods=["POST","GET"])
@login_required  
def text_to_picture_video():
    username=session.get("name")
    if request.method == "POST":
        data = request.get_json()
        type_name=data['type']
        text=data['text']
        if 'picture' in type_name:
            ####  post  ####
            logger.info('generate pic ing')
            url_self_media= 'https://83440n0z70.vicp.fun/image/FLUX_1_dev/generate'
            json_data_picture = {
                "prompt": text,
                "filename": "demo",
                "upload_to_cdn": True,
                "bucket_name": "wwa-test",
                "expire_time": 3600
            }
            # 发送请求并存储响应
            response_self_media = requests.post(url_self_media, json=json_data_picture)
            logger.info(response_self_media.text)
            self_media_res=response_self_media.json()
            choose_dict={}
            choose_dict['result']=0
            pic_status=''
            choose_dict['content']=pic_status
            if self_media_res['success']:
                url_link=self_media_res['data']['url']
                logger.info(url_link)
                #url_link="http://sicmnykdc.hd-bkt.clouddn.com/png/257d42325be94c7fada905650e5d0fac.png"
                tiem_str=str(datetime.datetime.today())
                file_pic=text+'_'+tiem_str+'.png'
                file_pic=file_pic.replace(' ','_').replace(':','').replace('-','')
                file_path_pic=os.path.join(current_app.config['UPLOAD_FOLDER_PIC'], file_pic)
                urllib.request.urlretrieve(url_link, file_path_pic)
                choose_dict['result']=1
            else:
                url_link='no find'
            pic_status='generate ok, check link:'+str(url_link)
            choose_dict['content']=pic_status
            return jsonify(choose_dict)
        elif 'video' in type_name:
            ####  post  ####
            url_self_media= 'https://83440n0z70.vicp.fun/video/CogVideoX_2b/generate'
            json_data_picture = {
                "prompt": text,
                "filename": "demo",
                "upload_to_cdn": True,
                "bucket_name": "wwa-test",
                "expire_time": 3600
            }
            # 发送请求并存储响应
            logger.info('generate vedio ing')
            response_self_media = requests.post(url_self_media, json=json_data_picture)
            self_media_res=response_self_media.json()
            choose_dict={}
            choose_dict['result']=0
            choose_dict['content']=''
            if self_media_res['success']:
                url_link=self_media_res['data']['url']
                logger.info(url_link)
                tiem_str=str(datetime.datetime.today())
                file_video=text+'_'+tiem_str+'.mp4'
                file_vedio=file_video.replace(' ','_').replace(':','').replace('-','')
                file_path_video=os.path.join(current_app.config['UPLOAD_FOLDER_VIDEO'], file_vedio)
                urllib.request.urlretrieve(url_link, file_path_video)
                choose_dict['result']=1
            else:
                url_link='no find'
            video_status='generate ok, check link:'+str(url_link)
            choose_dict['content']=video_status
            return jsonify(choose_dict)
    return render_template('text_to_picture_video.html',username=username)

@bp.route('/submit_pic',methods=["POST","GET"])
@login_required  
def submit_pic():
    if request.method == "POST":
        data = request.get_json()
        if 'selec_pic' in data['Type']:
            filepath=current_app.config['UPLOAD_FOLDER_PIC']
            files=os.listdir(filepath)
            file_dict={}
            file_dict['list']=files
            return jsonify(file_dict)
        elif 'add_pic' in data['Type']:#qpic
            access_token=os.getenv('access_token')
            filename=data['pic_file']
            pic_path=os.path.join(current_app.config['UPLOAD_FOLDER_PIC'], filename)
            logger.info(pic_path)
            ####  post  ####
            url_self_media= 'http://127.0.0.1:6050/wpp/upload_img'
            json_data_self_media = {
                "access_token": access_token,
                "file_path": pic_path
            }
            # 发送请求并存储响应
            response_self_media = requests.post(url_self_media, json=json_data_self_media)
            self_media_res=response_self_media.json()
            upload_status='upload qpic fail'
            choose_dict={}
            choose_dict['result']=0
            choose_dict['content']=upload_status
            if self_media_res['success']:
                choose_dict['content']=self_media_res['data']['url']
                choose_dict['result']=1
            return jsonify(choose_dict)
        elif 'submit_pic' in data['Type']:#wpp
            access_token=os.getenv('access_token')
            filename=data['pic_file']
            pic_path=os.path.join(current_app.config['UPLOAD_FOLDER_PIC'], filename)
            logger.info(pic_path)
            logger.info(access_token)
            ####  post  ####
            url_self_media= 'http://127.0.0.1:6050/wpp/material_img_add'
            json_data_self_media = {
                "access_token": access_token,
                "file_path": pic_path
            }
            # 发送请求并存储响应
            response_self_media = requests.post(url_self_media, json=json_data_self_media)
            self_media_res=response_self_media.json()
            upload_status='wpp fail'
            choose_dict={}
            choose_dict['result']=0
            choose_dict['content']=upload_status
            if self_media_res['success']:
                choose_dict['content']='okk'
                choose_dict['result']=1
                new_picture = weibo_Pic_Model()
                new_picture.name     = filename
                new_picture.media_id = self_media_res['data']['media_id']
                new_picture.url      = self_media_res['data']['url']
                db.session.add(new_picture)
                db.session.commit()
            return jsonify(choose_dict)
            
@bp.route('/submit_video',methods=["POST","GET"])
@login_required  
def submit_video():
    if request.method == "POST":
        data = request.get_json()
        if 'selec_vedio' in data['Type']:
            filepath=current_app.config['UPLOAD_FOLDER_VIDEO']
            files=os.listdir(filepath)
            file_dict={}
            file_dict['list']=files
            return jsonify(file_dict)
        elif 'submit_vedio' in data['Type']:
            access_token=os.getenv('access_token')
            filename=data['video_file']
            introduction=data['introduction']
            Video_Media_title=data['Video_Media_title']
            pic_path=os.path.join(current_app.config['UPLOAD_FOLDER_VIDEO'], filename)
            #print(pic_path)
            ####  post  ####
            url_self_media= 'http://127.0.0.1:6050/wpp/material_video_add'
            json_data_self_media = {
                "access_token": access_token,
                "file_path": pic_path,
                "title": Video_Media_title,
                "introduction": introduction
            }
            # 发送请求并存储响应
            response_self_media = requests.post(url_self_media, json=json_data_self_media)
            self_media_res=response_self_media.json()
            choose_dict={}
            choose_dict['result']=0
            if self_media_res['success']:
                #choose_dict['media_id']=self_media_res['data']['media_id']
                choose_dict['result']=1
                new_vedio = weibo_Vedio_Model()
                new_vedio.name              = filename
                new_vedio.media_id          = self_media_res['data']['media_id']
                new_vedio.title             = Video_Media_title
                new_vedio.introduction      = introduction
                db.session.add(new_vedio)
                db.session.commit()
            return jsonify(choose_dict)         

@bp.route('/get_token',methods=["POST","GET"])
@login_required  
def get_token():
    if request.method == "POST":
        data = request.get_json()
        if 'get_token' in data['Type']:
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
            choose_dict={}
            choose_dict['result']=0
            choose_dict['content']=token_status
            if self_media_res['success']:
                choose_dict['content']=self_media_res['data']['stable_access_token']['access_token']
                choose_dict['result']=1
            return jsonify(choose_dict)
        elif 'update_token' in  data['Type']:
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
            choose_dict={}
            choose_dict['result']=0
            choose_dict['content']=token_status
            if self_media_res['success']:
                choose_dict['content']=self_media_res['data']['stable_access_token']['access_token']
                file_path =current_app.config['VAR_FILE_PATH']
                new_line=[]
                with open(file_path, 'r') as file:
                    lines = file.readlines()
                    for item in lines:
                        if 'access_token=' in item:
                            str_line='access_token='+choose_dict['content']
                            new_line.append(str_line)
                        else:
                            new_line.append(item)
                # 将修改后的内容写回文件
                with open(file_path, 'w') as file:
                    file.writelines(new_line)
                choose_dict['result']=1
            return jsonify(choose_dict)        
          

#################################################################
############     2、 新建草稿
#################################################################
@bp.route('/draft_add',methods=["POST","GET"])
@login_required  
def draft_add():
    username=session.get("name")
    if request.method == "POST":
        data = request.get_json()
        if 'submit' in data['Type']:
            access_token=os.getenv('access_token')
            Title=data['Title']
            content=data['content']
            thumb_media_id=data['thumb_media_id']
            digest=data['digest']
            content_source_url=data['content_source_url']
            choose_dict={}
            choose_dict['result']=0
            ####  post  ####
            url_self_media= 'http://127.0.0.1:6050/wpp/draft_add'
            json_data_self_media = {
                "access_token": access_token,
                "title": Title,
                "author": username,
                "digest": digest,
                "content": content,
                "content_source_url": content_source_url,
                "thumb_media_id": thumb_media_id,
                "need_open_comment": 1,
                "only_fans_can_comment": 0
            }
            # 发送请求并存储响应
            logger.info('submit draft')
            logger.info(Title)
            logger.info(content)
            logger.info(thumb_media_id)
            response_self_media = requests.post(url_self_media, json=json_data_self_media)
            self_media_res=response_self_media.json()
            if self_media_res['success']:
                choose_dict['result']=1
                new_wpp_draft = weibo_wpp_add_draft_Model()
                new_wpp_draft.title               = re.sub('[^\u4e00-\u9fa5]+','',Title) #去除不可见字符
                new_wpp_draft.user                = username
                new_wpp_draft.thumb_media_id      = thumb_media_id
                new_wpp_draft.media_id            = self_media_res['data']['media_id']
                new_wpp_draft.digest              = re.sub('[^\u4e00-\u9fa5]+','',digest) #去除不可见字符
                new_wpp_draft.content             = re.sub('[^\u4e00-\u9fa5]+','',content) #去除不可见字符
                new_wpp_draft.content_source_url  = content_source_url
                db.session.add(new_wpp_draft)
                db.session.commit()
            return jsonify(choose_dict)
        elif 'selec_pic' in data['Type']:
            item_list = weibo_Pic_Model.query.all()
            Pic_lists = []
            choose_dict={}
            for item in item_list:
                temp_dict={}
                temp_dict['pic']=item.name
                temp_dict['thumb_media_id']=item.media_id
                Pic_lists.append(temp_dict)
            choose_dict['content']=Pic_lists
            return jsonify(choose_dict)
        elif 'generate' in data['Type']:
            Title=data['Title']
            format=data['format']
            digest=data['digest']
            type_name=data['type_name']
            model_select=data['model_name']
            if '2' in format:#小红书
                base_prompt = """
                帮我生成一篇关于`{}`
                的小红书种草文案。文案需要包含标题和正文，需要使用多种 emoji 来增强视觉吸引力和情感表达，内容包括`{}`
                """.strip()
                prompt = base_prompt.format('\n'.join(Title), digest)
            elif '3' in format:
                content_req='幽默'
                total_req='言辞生动活泼、富有感染力'
                target_people='年轻人'
                base_prompt = """
                帮我写一篇公众号文章，要求如下：
                公众号主题：`{}`
                公众号文章名称：`{}`。
                公众号内容要求：以生动的语言描述主题魅力，突出`{}`，吸引读者关注。
                整体风格要求：`{}`。
                目标读者群体为：`{}`
                """.strip()
                prompt = base_prompt.format('\n'.join(digest), Title,content_req,total_req,target_people)
            url = 'http://127.0.0.1:4010/private/inference'
            # 检查响应状态代码
            answer=no_vector_model_rag(url,prompt,type_name,model_select)
            res_result=''
            if answer['message'] == 'success':
                # 打印响应文本
                res_result=answer['data']['result']
            choose_dict={}
            choose_dict['result']=1
            choose_dict['res_result']=res_result
            return jsonify(choose_dict)
    return render_template('draft_add.html',username=username)

#################################################################
############     3、 发布文章
#################################################################
@bp.route('/self_media',methods=["POST","GET"])
@login_required
def self_media():
    if request.method == "POST":
        data = request.get_json()
        if 'publish' in data['Type']:
            MEDIA_ID=data['MEDIA_ID']
            access_token=os.getenv('access_token')
            # 检查响应状态代码
            ####  post  ####
            url_self_media= 'http://127.0.0.1:6050/wpp/publish_free'
            json_data_self_media = {
                "access_token": access_token,
                "MEDIA_ID": MEDIA_ID
            }
            # 发送请求并存储响应
            response_self_media = requests.post(url_self_media, json=json_data_self_media)
            self_media_res=response_self_media.json()
            choose_dict={}
            choose_dict['result']=0
            if self_media_res['success']:
                choose_dict['result']=1
                #choose_dict['content']=response
                return jsonify(choose_dict)
        elif 'selec_media_id' in data['Type']:
            item_list = weibo_wpp_add_draft_Model.query.all()
            Wpp_lists = []
            choose_dict={}
            for item in item_list:
                temp_dict={}
                temp_dict['title']               = item.title               
                temp_dict['author']              = item.user              
                temp_dict['thumb_media_id']      = item.thumb_media_id      
                temp_dict['media_id']            = item.media_id            
                temp_dict['digest']              = item.digest              
                temp_dict['content']             = item.content             
                temp_dict['content_source_url']  = item.content_source_url
                Wpp_lists.append(temp_dict)
            choose_dict['content']=Wpp_lists
            return jsonify(choose_dict)
    username=session.get("name")
    return render_template('self_media.html',username=username)
######################################################################################
# 智能微博
######################################################################################

#################################################################
############     1、 微博草稿
#################################################################
@bp.route('/weibo_choose_model',methods=["POST","GET"])
@login_required  
def weibo_choose_model():
    if request.method == "POST":
        data = request.get_json()
        type_name=data['type_name']
        model_type=['-- pls choose --']
        kb_list_content=[]
        if "choose_type" in type_name:
            try:
                res=os.popen("ps -ef | grep ollama").read()
                if 'ollama serve' in res:
                    model_type.append("ollama")
            except:
                logger.info('no ollama')
            try:
                res=os.popen("ps -ef | grep xinference").read()
                if 'xinference' in res:
                    model_type.append("xinference")
            except:
                logger.info('no xinference')
            choose_dict={}
            choose_dict['result']=1
            choose_dict['content']=model_type
            return jsonify(choose_dict)
        elif "choose_model" in type_name:
            type_select=data['type_select']
            model_list=[]
            if "ollama" in type_select:
                try:
                    res=os.popen("ollama list").read()
                    models=res.split('\n')
                    for index_i, item_i in enumerate(models):
                        if index_i == 0:
                            continue
                        model_list.append(item_i.split()[0])
                        print(item_i.split()[0])
                except:
                    logger.info('no ollama')
            choose_dict={}
            choose_dict['result']=1
            choose_dict['content']=model_list
            return jsonify(choose_dict)
        elif "choose_KB" in type_name:
            try:
                res=kb_list()
                kb_list_content=res['data']['kb_list']
            except:
                logger.info('no get kb list')
            choose_dict={}
            choose_dict['result']=1
            choose_dict['content']=kb_list_content
            return jsonify(choose_dict)
    else:
        username=session.get("name")
        return render_template('weibo_daily.html',username=username)

@bp.route('/weibo_model_run',methods=["POST"])
@login_required  
def weibo_model_run():
    if request.method == "POST":
        data = request.get_json()
        if 'run' in data['Type']:
            type_name=data['type_name']
            model_select=data['model_name']
            KB_id=data['KB_id']
            top_selector=data['top_selector']
            top_K=int(top_selector)
            query=data['query']
            base_prompt = """
            请根据案例```
            {}
            ```
            编写一个80字左右的法律科普微博，文案需要包含标题和正文，需要使用多种 emoji 来增强视觉吸引力和情感表达
                """.strip()
            prompt = base_prompt.format('\n\n'.join(query))
            logger.info(query)
            logger.info(prompt)
            if KB_id=='0':
                url = 'http://127.0.0.1:4010/private/inference'
                # 检查响应状态代码
                rag_result=''
                retrieve_result=''
                answer=no_vector_model_rag(url,prompt,type_name,model_select)
                if answer['message'] == 'success':
                    # 打印响应文本
                    rag_result=answer['data']['result']
                    retrieve_result='(no select vector)'
            else:
                url = 'http://127.0.0.1:7020/inference'
                # 检查响应状态代码
                rag_result=''
                retrieve_result=''
                answer=vector_model_rag(url,KB_id,top_K,prompt,type_name,model_select)
                if answer['message'] == 'success':
                    # 打印响应文本
                    rag_result=answer['data']['rag_result']
                    retrieve_result=answer['data']['retrieve_result'][0][0]['entity']['text']
            choose_dict={}
            choose_dict['result']=1
            choose_dict['rag_result']=rag_result
            choose_dict['retrieve_result']=retrieve_result
            #choose_dict['content']=response
            return jsonify(choose_dict)
        elif 'copy' in data['Type']:
            answer=data['answer']
            pyperclip.copy(answer)
            choose_dict={}
            choose_dict['result']=1
            #choose_dict['content']=response
            return jsonify(choose_dict)
#################################################################
############     2、 新浪微博
#################################################################