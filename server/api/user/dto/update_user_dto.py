from typing import Optional

from pydantic import field_validator
from api.user.dto import CreateUserDTO
from api.utils.validators import password_validator


class UpdateUserDTO(CreateUserDTO):
    password: Optional[str] = None

    @field_validator('password')
    def password_validation(cls, value: str | None) -> str:
        if value is None:
            return value

        return password_validator(value)
