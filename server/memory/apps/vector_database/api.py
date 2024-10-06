import requests


def get_embeddings(sentences):
    url = 'http://127.0.0.1:4020/inference_mul'
    res = requests.post(url, json={"sentences": sentences})
    return res.json()['data']['embeddings']


def get_docx2text(docx_path):
    url = 'http://127.0.0.1:7030/document/docx_to_text'
    res = requests.post(url, json={
        "doc_id": "doc_id",
        "doc_name": "doc_name",
        "doc_path": docx_path
    })
    return res.json()['data']['result']


def get_docx2chunks(docx_path):
    url = 'http://127.0.0.1:7030/document/docx_to_chunks'
    res = requests.post(url, json={
        "doc_id": "doc_id",
        "doc_name": "doc_name",
        "doc_path": docx_path
    })
    return res.json()['data']['result']


def run():
    doc_path = input('doc_path: ')
    doc_text = get_docx2text(doc_path)
    print(doc_text)


if __name__ == '__main__':
    run()
