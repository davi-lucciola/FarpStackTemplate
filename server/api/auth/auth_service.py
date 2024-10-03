from dataclasses import dataclass
from fastapi import Depends, HTTPException, status
from api.utils import jwt
from api.auth.strategies import (
    LoginStrategies,
    LoginStrategyFactory,
)
from api.auth.dto import LoginDTO
from api.user.user_model import User
from api.user.user_service import UserService
from jose.exceptions import ExpiredSignatureError, JWTError


@dataclass
class AuthService:
    user_service: UserService = Depends(UserService)

    async def login(
        self, credentials: LoginDTO, login_strategy: LoginStrategies
    ) -> str:
        strategy = LoginStrategyFactory.get(self.user_service, login_strategy)
        token: str = await strategy.login(credentials)
        return token

    async def authenticate(self, token: str) -> User:
        try:
            payload: dict = jwt.decode_token(token)
        except ExpiredSignatureError:
            raise HTTPException(
                detail='Token Expirado.', status_code=status.HTTP_401_UNAUTHORIZED
            )
        except JWTError:
            raise HTTPException(
                detail='Token inválido.', status_code=status.HTTP_401_UNAUTHORIZED
            )

        try:
            user = await self.user_service.find_by_id(int(payload.get('sub')))
        except HTTPException:
            raise HTTPException(
                detail='Usuário não encontrado.',
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        return user
