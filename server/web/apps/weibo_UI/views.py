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
#vue3
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
        print(result)
        return result
#############################################
