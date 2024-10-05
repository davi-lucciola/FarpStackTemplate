from typing import Any
from sqlalchemy.dialects import sqlite
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.types import JSON, BigInteger


class IBaseModel(DeclarativeBase):
    type_annotation_map = {dict[str, Any]: JSON}

    def can_update(self, **kwargs: dict[str, Any]):
        raise NotImplementedError('Method "can_update" not implemented.')


Long = BigInteger().with_variant(sqlite.INTEGER(), "sqlite")
