# -*- coding: utf-8 -*-
# Standard library imports.
import os
import sqlite3
# Related third party imports.
from flask import Flask
from loguru import logger
# Local application/library specific imports.
from configs import config
from extends import (
    db,
)
from apps.demo.models import DemoModel
from apps.demo import bp as demo_bp
# TODO: Import new blueprint here


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    app.register_blueprint(demo_bp)
    # TODO: Register new blueprint here
    db.init_app(app)

    return app


app = create_app()

with app.app_context():
    db.create_all()

host = '0.0.0.0'
port = 5010
debug = True

logger.info('Server is up and running.')
logger.info('Please visit http://127.0.0.1:{}/demo/heartbeat to verify.'.format(port))

if __name__ == '__main__':
    app.run(debug=debug, host=host, port=port)
