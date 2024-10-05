from pydantic import BaseModel


class BasicResponse(BaseModel):
    detail: str
