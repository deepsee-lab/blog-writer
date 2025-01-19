import os
import json
from datetime import datetime
from pymilvus import MilvusClient
from apps.vector_database.api import get_embeddings
from dotenv import load_dotenv

load_dotenv()


data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "milvus_data")
if not os.path.exists(data_dir):
    os.makedirs(data_dir, exist_ok=True)

client = MilvusClient(
    uri=os.getenv('milvus_uri'),
    token=os.getenv('milvus_token'),
)


def do_kb_list_all():
    l = []
    for filename in os.listdir(data_dir):
        if filename.endswith('.json'):
            file = os.path.join(data_dir, filename)
            if os.path.isfile(file):
                with open(file, 'r', encoding='utf-8') as f:
                    d = json.load(f)
                    l.append(d)

    return l


def do_kb_query_mul(kb_ids):
    result = {}
    for kb_id in kb_ids:
        kb_file = os.path.join(data_dir, "{}.json".format(kb_id))
        d = {}
        if os.path.exists(kb_file):
            with open(os.path.join(data_dir, "{}.json".format(kb_id)), 'r', encoding='utf-8') as f:
                d = json.load(f)
                d.pop('kb_id', None)
        result[kb_id] = d
    return result


class MilvusClass:
    def __init__(self, kb_id: str):
        if not str(kb_id).startswith('kb_id_'):
            kb_id = 'kb_id_{}'.format(kb_id)
        self.kb_id = kb_id

    def create_collection(self, dim: int):
        if not client.has_collection(self.kb_id):
            client.create_collection(
                collection_name=self.kb_id,
                dimension=dim
            )

    def do_kb_add_one(self, kb_id, kb_name, kb_desc, vector_store_name, embedding_model_name, dim):
        # if kb_id != self.kb_id:
        #     raise Exception("kb_id not match")

        self.create_collection(dim)

        d = {
            "kb_id": self.kb_id,
            "kb_name": kb_name,
            "kb_desc": kb_desc,
            "vector_store_name": vector_store_name,
            "embedding_model_name": embedding_model_name,
            "dim": dim,
            "create_time": str(datetime.now()),
            "is_delete": 0,
        }
        with open(os.path.join(data_dir, "{}.json".format(self.kb_id)), 'w', encoding='utf-8') as f:
            json.dump(d, f, ensure_ascii=False, indent=4)

    def insert_data(self, data):
        client.insert(collection_name=self.kb_id, data=data)

    def search_vectors(self, query_vectors, top_k, filter, output_fields):
        results = client.search(
            collection_name=self.kb_id,
            data=query_vectors,
            filter=filter,
            limit=top_k,
            output_fields=output_fields,
        )
        return results


def run():
    # init
    kb_id = 'uuid0000000000000000000000000000'
    dim = 1024
    milvus_class = MilvusClass(kb_id)
    print('init ok')
    # create_collection
    milvus_class.create_collection(dim=dim)
    # insert_data
    sentences = [
        '你好',
        '好的',
        '谢谢',
    ]
    vectors = get_embeddings(sentences)
    data = [
        {"id": i, "vector": vectors[i], "text": sentences[i], "subject": "biology"}
        for i in range(len(vectors))
    ]
    milvus_class.insert_data(data)
    print('insert_data ok')
    # search
    query = '您好'
    query_vectors = get_embeddings([query])
    res = client.search(
        collection_name=kb_id,
        data=query_vectors,
        # filter="subject == 'biology'",
        limit=2,
        output_fields=["text", "subject"],
    )
    print('search res: {}'.format(res))


if __name__ == "__main__":
    run()
