from loguru import logger
from fastapi import APIRouter
from typing import Optional
from pydantic import BaseModel, Field
from apps.wpp.scripts.get_stable_access_token import get_stable_access_token
from apps.wpp.scripts.add_permanent_assets import (
    uploadimg,
    add_material_img,
    add_material_video,
)
from apps.wpp.scripts.add_draft import add_draft
from apps.wpp.scripts.free_publish import free_publish

router = APIRouter(
    prefix="/wpp"
)


class DraftAddItem(BaseModel):
    access_token: str
    title: str = Field(default="title")
    author: Optional[str] = Field(default=None)
    digest: Optional[str] = Field(default=None)
    content: str = Field(default="content")
    content_source_url: Optional[str] = Field(default=None)
    thumb_media_id: str = Field(default="thumb_media_id")
    need_open_comment: Optional[int] = Field(default=1)
    only_fans_can_comment: Optional[int] = Field(default=0)


class StableAccessTokenItem(BaseModel):
    appid: str
    secret: str


class MaterialItem(BaseModel):
    access_token: str
    file_path: str


class VideoMaterialItem(MaterialItem):
    title: str
    introduction: str


class PublishItem(BaseModel):
    access_token: str
    MEDIA_ID: str


class Response(BaseModel):
    success: bool
    code: str
    message: str
    data: dict


@router.get("/heartbeat")
def heartbeat():
    logger.info('run heartbeat')
    return 'heartbeat'


@router.post("/stable_access_token_get")
def stable_access_token_get(item: StableAccessTokenItem):
    logger.info('run get_stable_access_token')
    appid, secret = item.appid, item.secret
    stable_access_token = get_stable_access_token(appid, secret)
    data = {
        'stable_access_token': stable_access_token,
    }
    logger.info(data)
    return Response(success=True, code='000000', message='success', data=data)


@router.post("/upload_img")
def upload_img(item: MaterialItem):
    logger.info('run upload_img')
    access_token, file_path = item.access_token, item.file_path
    data = uploadimg(access_token, file_path)
    logger.info(data)
    return Response(success=True, code='000000', message='success', data=data)


@router.post("/material_img_add")
def material_img_add(item: MaterialItem):
    logger.info('run material_img_add')
    access_token, file_path = item.access_token, item.file_path
    data = add_material_img(access_token, file_path)
    logger.info(data)
    return Response(success=True, code='000000', message='success', data=data)


@router.post("/material_video_add")
def material_video_add(item: VideoMaterialItem):
    logger.info('run material_img_add')
    access_token, file_path, title, introduction = item.access_token, item.file_path, item.title, item.introduction
    data = add_material_video(access_token, file_path, title, introduction)
    logger.info(data)
    return Response(success=True, code='000000', message='success', data=data)


@router.post("/draft_add")
def draft_add(item: DraftAddItem):
    logger.info('run draft_add')
    logger.info(item)
    res = add_draft(**item.model_dump())
    logger.info(res)
    if 'errcode' in res:
        return Response(success=False, code=str(res['errcode']), message=res['errmsg'], data=res)
    else:
        return Response(success=True, code='000000', message='success', data=res)


@router.post("/publish_free")
def publish_free(item: PublishItem):
    logger.info('run publish_free')
    access_token, MEDIA_ID = item.access_token, item.MEDIA_ID
    data = free_publish(access_token, MEDIA_ID)
    logger.info('data: {}'.format(data))
    return Response(success=True, code='000000', message='success', data=data)
