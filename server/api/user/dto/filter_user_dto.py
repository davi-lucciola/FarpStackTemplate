from typing import Optional
from pydantic import BaseModel


class FilterUserDTO(BaseModel):
    search: Optional[str]
    fl_google_user: Optional[str]
