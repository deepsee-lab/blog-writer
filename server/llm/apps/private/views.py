# -*- coding: utf-8 -*-
# Standard library imports.
import time
from typing import List
# Related third party imports.
from loguru import logger
from pydantic import BaseModel, Field
from fastapi import APIRouter
# Local application/library specific imports.
from apps.private.llms.ollama_inference import inf
from apps.private.apis.llm_server.client_one_api import inf as inf_v2
from apps.private.apis.llm_server.client_one_api import get_embedding_list
from apps.private.apis.llm_server.client_xinference import re_rank

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


class EmbeddingItem(BaseModel):
    model: str = Field(default="bge-base-zh-v1.5")
    sentences: List[str] = Field(default=['文本1', 'text2'])


class RerankItem(BaseModel):
    model: str = Field(default="bge-reranker-base")
    query: str = Field(default="A man is eating pasta.")
    corpus: List[str] = Field(default=[
        "A man is eating food.",
        "A man is eating a piece of bread.",
        "The girl is carrying a baby.",
        "A man is riding a horse.",
        "A woman is playing violin."
    ])


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

    time1 = time.time()

    result = inf_v2(**item.model_dump())

    time2 = time.time()

    logger.info('result:{}'.format(result))
    logger.info('costs:{}s'.format(time2 - time1))

    data = {
        'result': result,
    }

    return Response(success=True, code='000000', message='success', data=data)


@router.post('/embeddings')
def embeddings(item: EmbeddingItem):
    logger.info('run embeddings')
    logger.info('item:{}'.format(item))

    time1 = time.time()

    embedding_list = get_embedding_list(**item.model_dump())

    time2 = time.time()

    logger.debug('embeddings:{}'.format(embeddings))
    logger.info('costs:{}s'.format(time2 - time1))

    data = {
        'embeddings': embedding_list
    }

    return Response(success=True, code='000000', message='success', data=data)


@router.post('/rerank')
def rerank(item: RerankItem):
    logger.info('run rerank')
    logger.info('item:{}'.format(item))

    time1 = time.time()

    result = re_rank(**item.model_dump())

    time2 = time.time()

    logger.info('result:{}'.format(result))
    logger.info('costs:{}s'.format(time2 - time1))

    data = {
        'result': result
    }

    return Response(success=True, code='000000', message='success', data=data)


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
