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
