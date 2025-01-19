import uuid
from typing import List
from loguru import logger
from fastapi import APIRouter
from pydantic import BaseModel, Field
from apps.vector_database.vector_store.milvus_class import MilvusClass, client
from apps.vector_database.api import (
    get_embeddings,
    get_docx2text,
    get_docx2chunks,
)
from apps.vector_database.vector_store.milvus_class import (
    do_kb_list_all,
    do_kb_query_mul,
)

router = APIRouter(
    prefix="/vector"
)


class KbBaseItem(BaseModel):
    kb_id: str = Field(description='32-bit UUID without -', default='uuid' + '0' * 28)


class KbAddItem(KbBaseItem):
    kb_name: str = Field(default="kb_name")
    kb_desc: str = Field(default="kb_desc")
    vector_store_name: str = Field(default="milvus")
    embedding_model_name: str = Field(default="bge-large-zh-v1.5")
    dim: int = Field(default=1024)


class KbIdsItem(BaseModel):
    kb_ids: List[str] = Field(description='32-bit UUID without -', default=['uuid' + '0' * 28])


class TextBlockItem(BaseModel):
    text: str = Field(default="text")
    embedding: List[float]


class DocBaseItem(KbBaseItem):
    doc_id: str = Field(description='32-bit UUID without -', default='0' * 32)


class DocAddItem(DocBaseItem):
    doc_name: str = Field(default="doc_name")
    doc_path: str = Field(default="doc_path")
    doc_content_base64: str = Field(default="doc_content_base64")


class DocDropItem(KbBaseItem):
    doc_ids: List[str] = Field(default=['0' * 32])


class SearchItem(BaseModel):
    kb_id: str = Field(description='32-bit UUID without -', default='uuid' + '0' * 28)
    query: str
    top_k: int = Field(default=5)
    output_fields: List[str] = Field(default=["text"])


class Response(BaseModel):
    success: bool
    code: str
    message: str
    data: dict


@router.get("/heartbeat")
def heartbeat():
    logger.info('run heartbeat')
    return 'heartbeat'


@router.get("/kb_list_all")
def kb_list_all():
    logger.info('run kb_list_all')
    kb_list = do_kb_list_all()
    data = {
        'kb_list': kb_list,
    }
    return Response(success=True, code='000000', message='success', data=data)


@router.post("/kb_add_one")
def kb_add_one(item: KbAddItem):
    logger.info('run kb_add_one')
    logger.info(item)
    kb_id = item.kb_id
    milvus_class = MilvusClass(kb_id)
    milvus_class.do_kb_add_one(**item.model_dump())
    return Response(success=True, code='000000', message='success', data={})


@router.post("/kb_query_mul")
def kb_query_mul(item: KbIdsItem):
    logger.info('run kb_query_one')
    logger.info(item)
    kb_ids = item.kb_ids
    data = do_kb_query_mul(kb_ids)
    return Response(success=True, code='000000', message='success', data=data)


@router.post("/kb_del_mul")
def kb_del_mul(item: KbIdsItem):
    logger.info('run kb_del_one')
    logger.info(item)
    kb_list = [
        {
            "kb_id": "kb_id",
            "kb_name": "kb_name",
            "kb_desc": "kb_desc",
            "vector_store_name": "vector_store_name",
            "embedding_model_name": "embedding_model_name",
        }
    ]
    data = {
        'kb_list': kb_list,
    }
    return Response(success=True, code='000000', message='success', data=data)


@router.post("/doc_list_all")
def doc_list_all(item: KbBaseItem):
    logger.info('run doc_list_all')
    logger.info(item)
    kb_list = [
        {
            "doc_id": "doc_id",
            "doc_name": "doc_name",
            'doc_path': 'doc_path',
        }
    ]
    data = {
        'kb_id': 'kb_id',
        'doc_list': kb_list,
    }
    return Response(success=True, code='000000', message='success', data=data)


@router.post("/doc_add_one")
def doc_add_one(item: DocAddItem):
    milvus_class = MilvusClass(item.kb_id)
    logger.info('run doc_add_one')
    logger.info(item)
    doc_path = item.doc_path
    # chunks = get_docx2chunks(doc_path)
    text = get_docx2text(doc_path)
    sentences = str(text).split('。')
    chunks = ['{}。'.format(x) for x in sentences]
    vectors = get_embeddings(chunks)
    data = [
        {"id": i, "vector": vectors[i], "text": chunks[i], "subject": "biology"}
        for i in range(len(vectors))
    ]
    milvus_class.insert_data(data)
    return Response(success=True, code='000000', message='success', data={})


@router.post("/doc_query_one")
def doc_query_one(item: DocBaseItem):
    logger.info('run doc_query_one')
    logger.info(item)
    doc = {
        'doc_name': 'doc_name',
        'doc_id': 'doc_id',
        'doc_path': 'doc_path',
        'full_text': 'full_text',
        'text_blocks': [
            {
                'text': 'text',
                'embedding': [0.1, 0.2, 0.3],
            }
        ],
    }
    data = {
        'kb_id': 'kb_id',
        'doc': doc,
    }
    return Response(success=True, code='000000', message='success', data=data)


@router.post("/doc_del_mul")
def doc_del_mul(item: DocDropItem):
    logger.info('run kb_del_one')
    logger.info(item)
    kb_list = [
        {
            "doc_id": "doc_id",
            "doc_name": "doc_name",
            'doc_path': 'doc_path',
        }
    ]
    data = {
        'kb_id': 'kb_id',
        'doc_list': kb_list,
    }
    return Response(success=True, code='000000', message='success', data=data)


@router.post("/search")
def search(item: SearchItem):
    logger.info('run search')
    logger.info(item)
    kb_id = item.kb_id
    query = item.query
    top_k = item.top_k
    output_fields = item.output_fields
    query_vectors = get_embeddings([query])
    results = client.search(
        collection_name=kb_id,
        data=query_vectors,
        limit=top_k,
        output_fields=output_fields,
    )
    data = {
        'results': results
    }
    return Response(success=True, code='000000', message='success', data=data)
