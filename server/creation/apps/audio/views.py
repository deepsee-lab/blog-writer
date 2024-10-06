# -*- coding: utf-8 -*-
# Standard library imports.
# Related third party imports.
from loguru import logger
from fastapi import APIRouter
from pydantic import BaseModel, Field
# Local application/library specific imports.
from apps.audio.algorithm.stable_audio_1.stable_audio_open_1_0 import inf
from apis.cdn.upload import upload

router = APIRouter(
    prefix="/audio"
)


class GenerateItem(BaseModel):
    prompt: str = Field(default='128 BPM tech house drum loop.')
    negative_prompt: str = Field(default='Low quality.')
    audio_end_in_s: float = Field(default=10.0)
    filename: str = Field(default='demo')
    # cdn
    upload_to_cdn: bool = Field(default=True)
    bucket_name: str = Field(default='wwa-test')
    expire_time: int = Field(default=3600)


class Response(BaseModel):
    success: bool
    code: str
    message: str
    data: dict


@router.get("/heartbeat")
def heartbeat():
    logger.info('run heartbeat')
    return 'heartbeat'


@router.post("/stable_audio_open_1_0/generate")
def generate(item: GenerateItem):
    logger.info('run generate')
    logger.info('item: {}'.format(item))
    output_file = inf(item.prompt, item.negative_prompt, item.audio_end_in_s, item.filename)
    logger.info('output_file: {}'.format(output_file))
    if item.upload_to_cdn:
        url = upload(item.bucket_name, output_file, item.expire_time)
        data = {
            'url': url
        }
    else:
        data = {
            'output_file': output_file
        }
    logger.info('data: {}'.format(data))
    return Response(success=True, code='000000', message='success', data=data)
