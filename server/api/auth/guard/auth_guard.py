from typing import List, Optional
from fastapi import Depends, Security, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from api.auth import SECURITY_BEARER
from api.roles import Roles
from api.auth.auth_service import AuthService
from api.user.user_model import User


class AuthGuard:
    """Guard to be used with FastAPI "Depends" to authorizate
    if the user have one of the roles


    Args:
        roles (List[Roles] | Roles | None):
            - Roles that the user must have

    Raises:
        HTTPException: Unauthorized and Forbidden HTTPException responses
    """

    def __init__(self, roles: List[Roles] | Roles | None = None) -> None:
        self.roles = roles

    async def __call__(
        self,
        auth_service: AuthService = Depends(AuthService),
        auth: Optional[HTTPAuthorizationCredentials] = Security(SECURITY_BEARER),
    ) -> User:
        user = await self.authenticate(auth_service, auth)

        if user.authorize(self.roles) is False:
            raise HTTPException(
                detail='Usuário não autorizado.', status_code=status.HTTP_403_FORBIDDEN
            )

        return user

    async def authenticate(
        self, auth_service: AuthService, auth: Optional[HTTPAuthorizationCredentials]
    ) -> User:
        if auth is None:
            raise HTTPException(
                detail='Usuário não autenticado.',
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        return await auth_service.authenticate(auth.credentials)

    def __hash__(self) -> int:
        return hash((type(self),))
