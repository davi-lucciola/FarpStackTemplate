from enum import Enum, auto
from abc import ABC, abstractmethod
from api.user.dto import CreateUserDTO
from api.user.user_model import User
from api.user.user_repository import UserRepository


class CreateUserStrategy(ABC):
    @abstractmethod
    async def create_user(self, user: CreateUserDTO) -> User:
        raise NotImplementedError('Create User Not Implemented')


class CreateUserStrategies(Enum):
    DEFAULT = auto()
    GOOGLE = auto()


from .default_strategy import DefaultCreateUserStrategy
from .google_strategy import GoogleCreateUserStrategy


class CreateUserStrategyFactory:
    create_user_strategies: dict[CreateUserStrategies, CreateUserStrategy] = {
        CreateUserStrategies.DEFAULT: DefaultCreateUserStrategy,
        CreateUserStrategies.GOOGLE: GoogleCreateUserStrategy,
    }

    @classmethod
    def get(
        cls, user_repository: UserRepository, strategy: CreateUserStrategies
    ) -> CreateUserStrategy:
        Strategy = cls.create_user_strategies.get(strategy)

        if Strategy is None:
            raise RuntimeError('Estratégia de criação de usuário não encontrada.')

        return Strategy(user_repository)
