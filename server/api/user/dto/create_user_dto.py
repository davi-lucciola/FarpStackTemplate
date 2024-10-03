from typing import List, Optional
from pydantic import BaseModel, field_validator
from api.roles import Roles
from api.utils.validators import email_validator, password_validator


class CreateUserDTO(BaseModel):
    name: str
    email: str
    password: str
    profile_picture_uri: Optional[str] = None
    roles: List[Roles] = []

    @field_validator('email')
    def email_validation(cls, value: str) -> str:
        return email_validator(value)

    @field_validator('password')
    def password_validation(cls, value: str) -> str:
        return password_validator(value)
