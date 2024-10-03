from dataclasses import dataclass
from api.roles import Roles
from api.user.dto import CreateUserDTO
from api.user.user_model import User
from api.user.strategies import CreateUserStrategy
from api.user.user_repository import UserRepository


@dataclass
class GoogleCreateUserStrategy(CreateUserStrategy):
    user_repository: UserRepository

    async def create_user(self, user_dto: CreateUserDTO):
        user = User(
            user_dto.name,
            user_dto.email,
            profile_picture_uri=user_dto.profile_picture_uri,
        )

        user.password = None
        user.fl_google_user = True
        user.roles = [Roles.USER]

        user = await self.user_repository.save(user)
        return user
