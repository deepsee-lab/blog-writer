# -*- coding: utf-8 -*-
# Standard library imports.
# Related third party imports.
from loguru import logger
from fastapi import APIRouter
from pydantic import BaseModel, Field
# Local application/library specific imports.
from apps.document.algorithm import docx_parsing
from apps.document.algorithm import file_split

router = APIRouter(
    prefix="/document"
)


class DocxItem(BaseModel):
    doc_id: str = Field(default="doc_id")
    doc_name: str = Field(default="doc_name")
    doc_path: str = Field(description='relative_path: apps/document/algorithm/files/*.* or abs_file_path:/xxx/*.*',
                          default="doc_path")


class Response(BaseModel):
    success: bool
    code: str
    message: str
    data: dict


@router.get("/heartbeat")
def heartbeat():
    logger.info('run heartbeat')
    return 'heartbeat'


@router.post("/docx_to_json")
def docx_to_json(item: DocxItem):
    logger.info('item: {}'.format(item))
    doc_id = item.doc_id
    doc_name = item.doc_name
    doc_path = item.doc_path
    # TODO: fix "AttributeError: 'NoneType' object has no attribute 'replace'"
    result = docx_parsing.docx_to_json(doc_path)
    logger.info('result: {}'.format(result))
    data = {
        'doc_id': doc_id,
        'doc_name': doc_name,
        'doc_path': doc_path,
        'result': result,
    }
    return Response(success=True, code='000000', message='success', data=data)


@router.post("/docx_to_text")
def docx_to_text(item: DocxItem):
    logger.info('item: {}'.format(item))
    doc_id = item.doc_id
    doc_name = item.doc_name
    doc_path = item.doc_path
    result = docx_parsing.docx_to_text(doc_path)
    logger.info('result: {}'.format(result))
    data = {
        'doc_id': doc_id,
        'doc_name': doc_name,
        'doc_path': doc_path,
        'result': result,
    }
    return Response(success=True, code='000000', message='success', data=data)


@router.post("/docx_to_chunks")
def docx_to_chunks(item: DocxItem):
    logger.info('item: {}'.format(item))
    doc_id = item.doc_id
    doc_name = item.doc_name
    doc_path = item.doc_path
    result = docx_parsing.docx_to_text(doc_path)
    chunks = file_split.split_text(result)
    logger.info('result: {}'.format(chunks))
    data = {
        'doc_id': doc_id,
        'doc_name': doc_name,
        'doc_path': doc_path,
        'result': chunks,
    }
    return Response(success=True, code='000000', message='success', data=data)
