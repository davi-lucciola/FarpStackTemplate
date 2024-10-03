from typing import Optional, List
from pydantic import BaseModel
from api.roles import Roles


class UserDTO(BaseModel):
    id: int
    name: str
    email: str
    roles: List[Roles]
    profile_picture_uri: Optional[str]
    fl_google_user: bool

    class Config:
        from_attributes = True
