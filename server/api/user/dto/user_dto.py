from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from api.roles import Roles


class UserDTO(BaseModel):
    id: int
    name: str
    email: str
    roles: List[Roles]
    profile_picture_uri: Optional[str]
    fl_google_user: bool

    # Config
    model_config = ConfigDict(from_attributes=True)
