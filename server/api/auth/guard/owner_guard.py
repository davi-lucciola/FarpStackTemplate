from dataclasses import dataclass
from typing import List, Optional
from fastapi import Depends, Security, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from api.auth import SECURITY_BEARER
from api.roles import Roles
from api.auth.auth_service import AuthService
from api.user.user_model import User
from api.auth.guard import AuthGuard
from api.models import IBaseModel


@dataclass
class OwnerGuard(AuthGuard):
    """Guard to be used with FastAPI "Depends" to authorizate
    if the user have one of the roles or is owner of the resource


    Args:
        roles (List[Roles] | Roles | None):
            - Roles that the user must have

        model (IBaseModel):
            - Resource model to verify if the user is owner,
            need to implements "can_update" method

    Raises:
        HTTPException: Unauthorized and Forbidden HTTPException responses
    """

    def __init__(self, model: IBaseModel, roles: List[Roles] | Roles | None = None):
        self.model = model
        self.roles = roles

    async def __call__(
        self,
        id: int,
        auth_service: AuthService = Depends(AuthService),
        auth: Optional[HTTPAuthorizationCredentials] = Security(SECURITY_BEARER),
    ) -> User:
        user = await self.authenticate(auth_service, auth)

        owner_or_have_role = user.authorize(self.roles) or user.verify_owner(user_id=id)
        if not owner_or_have_role:
            raise HTTPException(
                detail='Usuário não autorizado.', status_code=status.HTTP_403_FORBIDDEN
            )

        return user

    def __hash__(self) -> int:
        return hash((type(self),))
