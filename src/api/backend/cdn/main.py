# -*- coding: utf-8 -*-
# Standard library imports.
import json
from typing import List
# Related third party imports.
import uvicorn
from loguru import logger
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
# Local application/library specific imports.
from configs import config
from scripts_cdn.qiniuyun_class import upload_file

app = FastAPI(
    title="CDN",
    description="CDN",
    version="0.0.1",
    docs_url="/docs",
    redoc_url="/redoc",
)
# 允许所有来源
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 允许访问的源列表
    allow_credentials=True,  # 支持 cookies 跨域
    allow_methods=["*"],  # 允许的请求方法
    allow_headers=["*"],  # 允许的请求头
)


class UploadItem(BaseModel):
    bucket_name: str = Field(default='wwa-test')
    localfile: str = Field(default='scripts/demo.txt')
    expire_time: int = Field(default=3600)


class Response(BaseModel):
    success: bool
    code: str
    message: str
    data: dict


@app.get("/")
def index():
    logger.info('index')
    return "index"


@app.get('/heartbeat')
def heartbeat():
    logger.info('run heartbeat')
    return 'heartbeat'


@app.post('/upload')
def upload(item: UploadItem):
    logger.info('run upload')
    logger.info('item: {}'.format(item))
    url = upload_file(bucket_name=item.bucket_name, localfile=item.localfile, expire_time=item.expire_time)
    logger.info('url: {}'.format(url))
    data = {'url': url}
    return Response(success=True, code='000000', message='success', data=data)


host = '0.0.0.0'
port = 6070
reload = True

logger.info('Server is up and running.')
logger.info('Browse http://127.0.0.1:{}/heartbeat to verify.'.format(port))
logger.info('Browse http://127.0.0.1:{}/docs to test.'.format(port))

if __name__ == '__main__':
    uvicorn.run(app="main:app", reload=reload, host=host, port=port)
