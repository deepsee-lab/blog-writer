import uvicorn
from loguru import logger
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apps.image.views import router as image_router
from apps.audio.views import router as audio_router
from apps.video.views import router as video_router
from configs import config

app = FastAPI(
    title="Creation",
    description="Creation",
    version="0.0.1",
    docs_url="/wb_ai/docs",
    redoc_url="/wb_ai/redoc",
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

app.include_router(image_router)
app.include_router(audio_router)
app.include_router(video_router)

host = '0.0.0.0'
port = 6060
reload = True

logger.info('Server is up and running.')
logger.info('Browse http://127.0.0.1:{} to verify.'.format(port))
logger.info('Browse http://127.0.0.1:{}/wb_ai/docs to test.'.format(port))

if __name__ == '__main__':
    uvicorn.run(app="main:app", reload=reload, host=host, port=port)
