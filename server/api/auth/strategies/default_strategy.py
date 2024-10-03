from dataclasses import dataclass
from fastapi import HTTPException, status
from api.utils import jwt
from api.auth.dto import LoginDTO
from api.auth.strategies import LoginStrategy
from api.user.user_service import UserService


@dataclass
class DefaultLoginStrategy(LoginStrategy):
    user_service: UserService

    async def login(self, credentials: LoginDTO) -> str:
        user = await self.user_service.find_by_email(credentials.email)

        if user is not None and user.fl_google_user is True and user.password is None:
            raise HTTPException(
                detail='Usuário associado a uma conta google sem senha cadastrada. Entre com o google.',
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        if user is None or user.check_password(credentials.password) is False:
            raise HTTPException(
                detail='Credenciais Inválidas.',
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        access_token = jwt.create_token(user.id)
        return access_token
