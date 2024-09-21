# -*- coding: utf-8 -*-
# Standard library imports.
import datetime
# Related third party imports.
from sqlalchemy.orm import Mapped, mapped_column
# Local application/library specific imports.
from extends import (
    db,
)
from configs import config

cst_tz = config.cst_tz


class DemoModel(db.Model):
    __tablename__ = 'demo'
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(db.String, nullable=False, unique=True)
    text: Mapped[str] = mapped_column(db.Text, nullable=True)
    create_time: Mapped[datetime.datetime] = mapped_column(
        db.DateTime,
        nullable=False,
        default=datetime.datetime.now(cst_tz)
    )
