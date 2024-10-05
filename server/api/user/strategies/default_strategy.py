from dataclasses import dataclass
from api.roles import Roles
from api.user.dto import CreateUserDTO
from api.user.user_model import User
from api.user.strategies import CreateUserStrategy
from api.user.user_repository import UserRepository


@dataclass
class DefaultCreateUserStrategy(CreateUserStrategy):
    user_repository: UserRepository

    async def create_user(self, user: CreateUserDTO):
        if Roles.USER not in user.roles:
            user.roles.append(Roles.USER)

        user = User(user.name, user.email, user.password, user.roles)
        return self.user_repository.save(user)
