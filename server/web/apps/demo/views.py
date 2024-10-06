# -*- coding: utf-8 -*-
# Standard library imports.
import sqlite3
# Related third party imports.
from flask import Flask, Blueprint
from loguru import logger

# Local application/library specific imports.


bp = Blueprint("demo", __name__, url_prefix='/demo')


@bp.route('/heartbeat')
def heartbeat():
    logger.info('run heartbeat')
    return 'heartbeat'
