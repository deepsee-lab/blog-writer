# -*- coding: utf-8 -*-
# Standard library imports.
# Related third party imports.
import uvicorn
from loguru import logger
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Local application/library specific imports.
from apps.document.views import router as document_router
from configs import config

app = FastAPI(
    title="File Parsing",
    description="File Parsing",
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

app.include_router(document_router)


@app.get("/")
def index():
    logger.info("index")
    return "index"


host = '0.0.0.0'
port = 7030
reload = True

logger.info('Server is up and running.')
logger.info('Browse http://127.0.0.1:{} to verify.'.format(port))
logger.info('Browse http://127.0.0.1:{}/docs to test.'.format(port))

if __name__ == '__main__':
    uvicorn.run(app="main:app", reload=reload, host=host, port=port)
