# -*- coding: utf-8 -*-
# Standard library imports.
from typing import Optional
# Related third party imports.
from loguru import logger
from fastapi import APIRouter
from pydantic import BaseModel, Field
# Local application/library specific imports.
from apps.video.algorithm.CogVideoX.CogVideoX_2b import inf as cog_videox_2b_inf
from apps.video.algorithm.CogVideoX.CogVideoX_5b import inf as cog_videox_5b_inf
from apps.audio.algorithm.stable_audio_1.stable_audio_open_1_0 import inf as stable_audio_open_1_0_inf
from apps.video.toolkit.add_audio_to_video import add_audio_to_video_cli
from apis.cdn.upload import upload
from apis.toolkit.translation.ByteDance import ch2en

router = APIRouter(
    prefix="/video"
)


class GenerateItem(BaseModel):
    prompt: str = Field(
        default="A detailed wooden toy ship with intricately carved masts and sails is seen gliding smoothly over a plush, blue carpet that mimics the waves of the sea. The ship's hull is painted a rich brown, with tiny windows. The carpet, soft and textured, provides a perfect backdrop, resembling an oceanic expanse. Surrounding the ship are various other toys and children's items, hinting at a playful environment. The scene captures the innocence and imagination of childhood, with the toy ship's journey symbolizing endless adventures in a whimsical, indoor setting."
    )
    translate: Optional[bool] = Field(default=True)
    translate_mode: Optional[str] = Field(default='ch2en')
    audio: Optional[bool] = Field(default=True)
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


@router.post("/CogVideoX_2b/generate")
def cog_videox_2b_generate(item: GenerateItem):
    logger.info('run generate')
    logger.info('item: {}'.format(item))
    prompt = item.prompt
    if item.translate and item.translate_mode == 'ch2en':
        prompt = ch2en(prompt)
    logger.info('prompt: {}'.format(prompt))
    filename = item.filename
    video_file = cog_videox_2b_inf(prompt, filename)
    logger.info('video_file: {}'.format(video_file))
    if item.audio:
        auido_prompt = prompt
        auido_negative_prompt = 'Low quality.'
        audio_end_in_s = 8
        audio_file = stable_audio_open_1_0_inf(auido_prompt, auido_negative_prompt, audio_end_in_s, filename)
        logger.info('audio_file: {}'.format(audio_file))
        output_file = video_file.replace('.mp4', '_with_audio.mp4')
        add_audio_to_video_cli(video_file, audio_file, output_file, overwrite=True)
    else:
        output_file = video_file
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


@router.post("/CogVideoX_5b/generate")
def cog_videox_5b_generate(item: GenerateItem):
    logger.info('run generate')
    logger.info('item: {}'.format(item))
    prompt = item.prompt
    if item.translate and item.translate_mode == 'ch2en':
        prompt = ch2en(prompt)
    logger.info('prompt: {}'.format(prompt))
    output_file = cog_videox_5b_inf(prompt, item.filename)
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
