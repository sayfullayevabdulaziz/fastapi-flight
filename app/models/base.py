from __future__ import annotations

import datetime
import re

from sqlalchemy import func
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


def camel_to_snake_case(name: str) -> str:
    pattern = re.compile(r'(?<!^)(?=[A-Z])')
    return pattern.sub('_', name).lower()


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    @declared_attr
    def __tablename__(cls) -> str:
        return camel_to_snake_case(cls.__name__)
