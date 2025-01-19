# -*- coding: utf-8 -*-
# Standard library imports.
import time
from typing import List, Any, Optional
# Related third party imports.
from loguru import logger
from pydantic import BaseModel, Field
from fastapi import APIRouter
# Local application/library specific imports.
from apps.private.llms.model_list import get_model_list
from apps.private.llms.inference import inf
from apps.private.llms.embedding import get_embedding_list
from apps.private.llms.rerank import re_rank
from apps.private.llms.image_generation import image_generation
from apis.cdn.upload import upload
from apis.toolkit.translation.ByteDance import ch2en

router = APIRouter(
    prefix="/private"
)


class ModelListItem(BaseModel):
    inference_service: str = Field(description="Choose from ollama, xinference, api...", default="ollama")


class MessageItem(BaseModel):
    role: str = Field(description="Choose from system, user, assistant...", default="user")
    content: Any = Field(description="prompt", default="hi")


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
    model: str = Field(default="nomic-embed-text:137m-v1.5-fp16")
    sentences: List[str]
    inference_service: str = Field(description="Choose from ollama, xinference, api...", default="ollama")


class RerankItem(BaseModel):
    model: str = Field(default="bge-reranker-base")
    query: str = Field(default="A man is eating pasta.")
    corpus: List[str]
    inference_service: str = Field(description="Choose from ollama, xinference, api...", default="xinference")


class GenerateItem(BaseModel):
    # llm
    filename: str = Field(default='demo')
    model: str = Field(default="FLUX.1-dev")
    prompt: str = Field(default='A cat holding a sign that says hello world')
    inference_service: str = Field(description="Choose from ollama, xinference, api...", default="xinference")
    # translate
    translate: Optional[bool] = Field(default=False)
    translate_mode: Optional[str] = Field(default='ch2en')
    # cdn
    upload_to_cdn: bool = Field(default=True)
    bucket_name: str = Field(default='ca-test')
    expire_time: int = Field(default=3600)


class Response(BaseModel):
    success: bool
    code: str
    message: str
    data: dict


@router.post('/models')
def models(item: ModelListItem):
    logger.info('run models')
    logger.info('item: {}'.format(item))

    all_model_list = get_model_list(**item.model_dump())
    data = {
        'all_model_list': all_model_list,
    }

    return Response(success=True, code='000000', message='success', data=data)


@router.post('/inference')
def inference(item: InfItem):
    logger.info('run inference')
    logger.info('item: {}'.format(item))

    result = inf(**item.model_dump())
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
def generate_image(item: GenerateItem):
    logger.info('run generate')
    logger.info('item: {}'.format(item))
    prompt = item.prompt
    if item.translate and item.translate_mode == 'ch2en':
        prompt = ch2en(prompt)
    logger.info('prompt: {}'.format(prompt))
    output_file = image_generation(item.filename, item.model, prompt, item.inference_service)
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


@router.post('/generate/video')
def generate_video(item: InfItem):
    pass


@router.get("/heartbeat")
def heartbeat():
    logger.info('run heartbeat')
    return 'heartbeat'
