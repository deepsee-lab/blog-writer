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

# DB
# sqlite
CUS_DB_PATH = os.path.join(ROOT_DIR, 'db.sqlite3')
SQLALCHEMY_DATABASE_URI = 'sqlite:////{}'.format(CUS_DB_PATH)
SQLALCHEMY_TRACK_MODIFICATIONS = False
