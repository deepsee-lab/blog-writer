import uvicorn
from loguru import logger
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apps.wpp.views import router as wpp_router
from configs import config

app = FastAPI(
    title="self_media",
    description="self_media",
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

app.include_router(wpp_router)


@app.get("/")
def index():
    logger.info("index")
    return "index"


host = '0.0.0.0'
port = 6050
reload = True

logger.info('Server is up and running.')
logger.info('Browse http://127.0.0.1:{} to verify.'.format(port))
logger.info('Browse http://127.0.0.1:{}/docs to test.'.format(port))

if __name__ == '__main__':
    uvicorn.run(app="main:app", reload=reload, host=host, port=port)
