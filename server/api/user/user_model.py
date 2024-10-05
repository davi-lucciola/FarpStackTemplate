from typing import Any, List
from typing import Optional
from api.utils import crypt
from api.roles import Roles
from api.user.dto import UpdateUserDTO
from api.models import IBaseModel, Long
from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column


class User(IBaseModel):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Long, primary_key=True, autoincrement=True)
    name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True, index=True)
    password: Mapped[Optional[str]]
    roles: Mapped[JSON] = mapped_column(type_=JSON)
    fl_google_user: Mapped[bool] = mapped_column(default=False)
    profile_picture_uri: Mapped[Optional[str]] = mapped_column(default=None)

    def __init__(
        self,
        name: str,
        email: str,
        password: str | None = None,
        roles: list[Roles] = [Roles.USER],
        fl_google_user: bool = False,
        profile_picture_uri: str | None = None,
    ):
        self.name = name
        self.email = email
        self.password = crypt.hash(password) if password is not None else password
        self.roles = roles
        self.fl_google_user = fl_google_user
        self.profile_picture_uri = profile_picture_uri

    def check_password(self, plain_password: str) -> bool:
        return crypt.check_hash(plain_password, self.password)

    def authorize(self, roles: Optional[List[Roles] | Roles]) -> bool:
        if roles is None:
            return True
        elif isinstance(roles, str) and roles in self.roles:
            return True
        elif isinstance(roles, list):
            for role in roles:
                if role in self.roles:
                    return True

        return False

    def update(self, user_dto: UpdateUserDTO) -> None:
        self.name = user_dto.name
        self.email = user_dto.email
        self.password = (
            crypt.hash(user_dto.password) if user_dto.password is not None else None
        )
        self.profile_picture_uri = user_dto.profile_picture_uri
        self.roles = user_dto.roles if len(user_dto.roles) != 0 else [Roles.USER]

    def can_update(self, **kwargs: dict[str, Any]):
        return self.id == kwargs.get('user_id')

    def __str__(self) -> str:
        return f'<User ({self.id}) - {self.name}>'
