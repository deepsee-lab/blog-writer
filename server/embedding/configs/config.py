# -*- coding: utf-8 -*-
# https://peps.python.org/pep-0008/
# Imports are always put at the top of the file, just after any module comments and docstrings, and before module globals and constants.
# Imports should be grouped in the following order:
# Standard library imports.
import os
import sys
# Related third party imports.
import pytz
from loguru import logger
from dotenv import load_dotenv

load_dotenv()

# Get ROOT_DIR
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Set logger
logger.remove()
log_dir = os.path.join(ROOT_DIR, 'logs')
log_file = os.path.join(log_dir, '{time:YYYY-MM-DD}.log')
log_level = 'INFO'
logger.add(sys.stderr, level=log_level)
logger.add(log_file, level=log_level, rotation="00:00", enqueue=True, serialize=False, encoding="utf-8")

# Print ROOT_DIR
logger.info('ROOT_DIR: {}'.format(ROOT_DIR))

# Set timezone
cst_tz = pytz.timezone('Asia/Shanghai')

# EMBEDDING
# MODEL_NAME = 'nvidia/NV-Embed-v1'
# MODEL_NAME = 'shibing624/text2vec-base-chinese'
# MODEL_NAME = 'moka-ai/m3e-small'
# MODEL_NAME = 'moka-ai/m3e-base'
# MODEL_NAME = 'moka-ai/m3e-large'
# MODEL_NAME = 'BAAI/bge-multilingual-gemma2'
# MODEL_NAME = 'BAAI/bge-small-en-v1.5'
# MODEL_NAME = 'BAAI/bge-base-en-v1.5'
# MODEL_NAME = 'BAAI/bge-large-en-v1.5'
# MODEL_NAME = 'BAAI/bge-m3'
# MODEL_NAME = 'BAAI/bge-small-zh-v1.5'
# MODEL_NAME = 'BAAI/bge-base-zh-v1.5'
MODEL_NAME = 'BAAI/bge-large-zh-v1.5'

logger.info('MODEL_NAME: {}'.format(MODEL_NAME))

MODEL_DIR = os.getenv('BASE_EMBEDDING_MODEL_DIR')
if not MODEL_DIR:
    raise ValueError('.env BASE_EMBEDDING_MODEL_DIR not set')
MODEL_PATH = os.path.join(MODEL_DIR, MODEL_NAME)
if os.path.exists(MODEL_PATH):
    logger.info('MODEL_PATH: {}'.format(MODEL_PATH))
else:
    logger.error('MODEL_PATH: {} not exists'.format(MODEL_PATH))
    raise FileNotFoundError('MODEL_PATH: {} not exists'.format(MODEL_PATH))
