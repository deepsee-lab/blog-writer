from pprint import pprint
from loguru import logger
from apps.private.llms.rerank import re_rank


def run():
    model = "bge-reranker-base"
    query = "A man is eating pasta."
    corpus = [
        "A man is eating food.",
        "A man is eating a piece of bread.",
        "The girl is carrying a baby.",
        "A man is riding a horse.",
        "A woman is playing violin."
    ]

    logger.info(f'model: {model}')
    logger.info(f'query: {query}')
    logger.info(f'corpus: {corpus}')
    pprint(corpus)

    inference_service = 'xinference'
    result = re_rank(model, query, corpus, inference_service)

    logger.info(f'result: {result}')
    pprint(result)


if __name__ == '__main__':
    run()
