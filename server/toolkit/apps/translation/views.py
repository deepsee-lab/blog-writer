from loguru import logger
from pydantic import BaseModel
from fastapi import APIRouter
from apps.translation.apis.ByteDance import run_ch2en, run_en2ch

router = APIRouter(
    prefix="/translation"
)


class TextItem(BaseModel):
    text: str


class Response(BaseModel):
    success: bool
    code: str
    message: str
    data: dict


@router.get("/heartbeat")
def heartbeat():
    logger.info('run heartbeat')
    return 'heartbeat'


@router.post("/ByteDance/ch2en")
def deepl_ch2en(item: TextItem):
    logger.info('run deepl_ch2en')
    logger.info('item: {}'.format(item))

    result = run_ch2en(item.text)
    data = {
        'result': result,
    }

    return Response(success=True, code='000000', message='success', data=data)


@router.post("/ByteDance/en2ch")
def deepl_en2ch(item: TextItem):
    logger.info('run deepl_en2ch')
    logger.info('item: {}'.format(item))

    result = run_en2ch(item.text)
    data = {
        'result': result,
    }

    return Response(success=True, code='000000', message='success', data=data)