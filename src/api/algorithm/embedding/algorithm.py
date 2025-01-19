from sentence_transformers import SentenceTransformer
from configs import config
from loguru import logger

model_path = config.MODEL_PATH
model = SentenceTransformer(model_path)

logger.info('Model loaded successfully.')


def inference(sentences):
    embeddings = model.encode(sentences, normalize_embeddings=True)
    return embeddings


def run():
    sentences_1 = ["样例数据-1", "样例数据-2"]
    sentences_2 = ["样例数据-3", "样例数据-4"]
    embeddings_1 = inference(sentences_1)
    embeddings_2 = inference(sentences_2)
    similarity = embeddings_1 @ embeddings_2.T

    logger.info('similarity: {}'.format(similarity))


if __name__ == '__main__':
    import time

    time1 = time.time()

    run()

    time2 = time.time()

    logger.info(f'total time: {time2 - time1}')
