# -*- coding: utf-8 -*-
# Standard library imports.
from typing import List
# Related third party imports.
from loguru import logger
from pydantic import BaseModel, Field
from fastapi import APIRouter
# Local application/library specific imports.
from apps.private.llms.ollama_inference import inf
from apps.private.apis.one_api_client import inf as inf_v2

router = APIRouter(
    prefix="/private"
)


class MessageItem(BaseModel):
    role: str = Field(description="Choose from system, user, assistant...", default="user")
    content: str = Field(default="prompt")


class InfBaseItem(BaseModel):
    messages: List[MessageItem] = Field(description="Please refer to openai to write")
    model: str = Field(default="qwen2.5:0.5b-instruct-fp16")
    max_tokens: int = Field(default=4096)
    stream: bool = Field(default=False)
    temperature: float = Field(default=0.8)
    timeout: int = Field(default=60)


class InfItem(InfBaseItem):
    inference_service: str = Field(description="Choose from ollama, xinference, api...", default="ollama")


class Response(BaseModel):
    success: bool
    code: str
    message: str
    data: dict


@router.post('/inference')
def inference(item: InfItem):
    logger.info('run inference')
    logger.info('item: {}'.format(item))

    result = inf(**item.model_dump())
    data = {
        'result': result,
    }

    return Response(success=True, code='000000', message='success', data=data)


@router.post('/inference/v2')
def inference_v2(item: InfBaseItem):
    logger.info('run inference_v2')
    logger.info('item: {}'.format(item))

    result = inf_v2(**item.model_dump())
    data = {
        'result': result,
    }

    return Response(success=True, code='000000', message='success', data=data)


@router.post('/embedding')
def embedding(item: InfItem):
    pass


@router.post('/rerank')
def rerank(item: InfItem):
    pass


@router.post('/generate/image')
def generate_image(item: InfItem):
    pass


@router.post('/generate/video')
def generate_video(item: InfItem):
    pass


@router.get("/heartbeat")
def heartbeat():
    logger.info('run heartbeat')
    return 'heartbeat'
