# -*- coding: utf-8 -*-
# Standard library imports.
import os
import traceback
# Related third party imports.
from loguru import logger
from openai import OpenAI
from dotenv import load_dotenv
from xinference_client import RESTfulClient as Client

load_dotenv()

logger.info('all llm client init start.')

# Online-API
# openai_client
try:
    base_url = os.getenv('ONLINE_OPENAI_API_BASE')
    api_key = os.getenv('ONLINE_OPENAI_API_KEY')
    if base_url is not None and api_key is not None:
        openai_client_online = OpenAI(
            base_url=base_url,
            api_key=api_key,
        )
        logger.info('openai_client_online init.')
except Exception as e:
    logger.error(e)
    logger.error(traceback.print_exc())
    # TODO: set startup or not.
    logger.error('check online openai api config in server/.env')

# One-API
# openai_client
try:
    base_url = os.getenv('ONE_API_BASE')
    api_key = os.getenv('ONE_API_KEY')
    if base_url is not None and api_key is not None:
        openai_client_one_api = OpenAI(
            base_url=base_url,
            api_key=api_key,
        )
        logger.info('openai_client_one_api init.')
except Exception as e:
    logger.error(e)
    logger.error(traceback.print_exc())
    logger.error('check one-api config in server/.env')

# Ollama
# openai_client
try:
    base_url = os.getenv('OLLAMA_API_BASE')
    api_key = os.getenv('OLLAMA_API_KEY')
    if base_url is not None and api_key is not None:
        openai_client_ollama = OpenAI(
            base_url=base_url,
            api_key=api_key,
        )
        logger.info('openai_client_ollama init.')
except Exception as e:
    logger.error(e)
    logger.error(traceback.print_exc())
    logger.error('check ollama config in server/.env')

# XINFERENCE
# openai_client
# xinference_client
OUTPUT_DATA_DIR = os.getenv('OUTPUT_DATA_DIR')
try:
    XINFERENCE_API_BASE = os.getenv('XINFERENCE_API_BASE')
    XINFERENCE_API_KEY = os.getenv('XINFERENCE_API_KEY')
    if XINFERENCE_API_BASE is not None and XINFERENCE_API_KEY is not None:
        openai_client_xinference = OpenAI(
            base_url=os.path.join(XINFERENCE_API_BASE, 'v1'),
            api_key=XINFERENCE_API_KEY,
        )
        xinference_client = Client(XINFERENCE_API_BASE, api_key=XINFERENCE_API_KEY)
        logger.info('openai_client_xinference init.')
        logger.info('xinference_client init.')
except Exception as e:
    logger.error(e)
    logger.error(traceback.print_exc())
    logger.error('check xinference config in server/.env')

logger.info('all llm client init finish.')
