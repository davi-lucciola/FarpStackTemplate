from enum import Enum, auto
from abc import ABC, abstractmethod
from api.auth.dto import LoginDTO
from api.user.user_service import UserService


class LoginStrategy(ABC):
    @abstractmethod
    async def login(self, credentials: LoginDTO) -> str:
        raise NotImplementedError('Login Method Not Implemented')


class LoginStrategies(Enum):
    DEFAULT = auto()
    GOOGLE = auto()


from .default_strategy import DefaultLoginStrategy
from .google_strategy import GoogleLoginStrategy


class LoginStrategyFactory:
    login_strategies: dict[LoginStrategies, LoginStrategy] = {
        LoginStrategies.DEFAULT: DefaultLoginStrategy,
        LoginStrategies.GOOGLE: GoogleLoginStrategy,
    }

    @classmethod
    def get(cls, user_service: UserService, strategy: LoginStrategies) -> LoginStrategy:
        Strategy = cls.login_strategies.get(strategy)

        if Strategy is None:
            raise RuntimeError('Estratégia de login não encontrada.')

        return Strategy(user_service)
