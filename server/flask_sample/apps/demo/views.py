# -*- coding: utf-8 -*-
# Standard library imports.
import sqlite3
# Related third party imports.
from flask import Blueprint, render_template
from loguru import logger

# Local application/library specific imports.


bp = Blueprint("demo", __name__, url_prefix='/demo')


@bp.route('/')
def index():
    logger.info('run index')
    return render_template('demo/index.html')


@bp.route('/heartbeat')
def heartbeat():
    logger.info('run heartbeat')
    return 'heartbeat'
