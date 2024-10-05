from typing import List
from fastapi import APIRouter, Depends, status
from api.utils import BasicResponse
from api.user.user_service import UserService
from api.user.dto import UserDTO, CreateUserDTO, UpdateUserDTO
from api.user.strategies import CreateUserStrategies
from api.user.user_model import User
from api.roles import Roles
from api.auth.guard import AuthGuard, OwnerGuard


user_router = APIRouter(prefix='/users', tags=['User'])


@user_router.post('/sign-up', status_code=status.HTTP_201_CREATED)
async def signup(
    user_dto: CreateUserDTO, user_service: UserService = Depends(UserService)
):
    user_dto.roles = []
    await user_service.create(user_dto, CreateUserStrategies.DEFAULT)

    return BasicResponse(detail='Usuário cadastrado com sucesso.')


@user_router.get('/', dependencies=[Depends(AuthGuard(Roles.ADMIN))])
async def get_all_users(
    user_service: UserService = Depends(UserService),
) -> List[UserDTO]:
    return await user_service.find_all()


@user_router.get('/{id}', dependencies=[Depends(OwnerGuard(User, Roles.ADMIN))])
async def get_user_by_id(
    id: int, user_service: UserService = Depends(UserService)
) -> UserDTO:
    return await user_service.find_by_id(id)


@user_router.post('/')
async def create_user(
    user_dto: CreateUserDTO,
    user: User = Depends(AuthGuard(Roles.ADMIN)),
    user_service: UserService = Depends(UserService),
):
    await user_service.create(user_dto, CreateUserStrategies.DEFAULT, user.roles)
    return BasicResponse(detail='Usuário cadastrado com sucesso.')


@user_router.put('/{id}')
async def update_user(
    id: int,
    user_dto: UpdateUserDTO,
    user: User = Depends(OwnerGuard(User, Roles.ADMIN)),
    user_service: UserService = Depends(UserService),
):
    await user_service.update(id, user_dto, user.roles)
    return BasicResponse(detail='Usuário atualizado com sucesso.')


@user_router.delete('/{id}', dependencies=[Depends(OwnerGuard(User, Roles.ADMIN))])
async def delete_user(id: int, user_service: UserService = Depends(UserService)):
    await user_service.delete(id)
    return BasicResponse(detail='Usuário excluído com sucesso.')
