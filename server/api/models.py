from typing import Any
from sqlalchemy.types import JSON
from sqlalchemy.orm import DeclarativeBase


class IBaseModel(DeclarativeBase):
    type_annotation_map = {dict[str, Any]: JSON}

    def can_update(self, **kwargs: dict[str, Any]):
        raise NotImplementedError("Method \"can_update\"not implemented.")