from dataclasses import dataclass
from fastapi import Depends, HTTPException, status
from api.roles import Roles
from api.user.user_model import User
from api.user.dto import CreateUserDTO, UpdateUserDTO
from api.user.user_repository import UserRepository
from api.user.strategies import CreateUserStrategies, CreateUserStrategyFactory


@dataclass
class UserService:
    user_repository: UserRepository = Depends(UserRepository)

    async def find_all(self) -> list[User]:
        return await self.user_repository.find_all()

    async def find_by_id(self, user_id: str) -> User:
        user = await self.user_repository.find_by_id(user_id)

        if user is None:
            raise HTTPException(
                detail='Usuário não encontrado.', status_code=status.HTTP_404_NOT_FOUND
            )

        return user

    async def find_by_email(self, email: str) -> User | None:
        return await self.user_repository.find_by_email(email)

    async def create(
        self, user_dto: CreateUserDTO, create_strategy: CreateUserStrategies
    ) -> User:
        exist_user = await self.user_repository.find_by_email(user_dto.email)

        if exist_user is not None:
            raise HTTPException(
                detail='Usuário já cadastrado com esse email.',
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        strategy = CreateUserStrategyFactory.get(self.user_repository, create_strategy)
        new_user = await strategy.create_user(user_dto)
        return new_user

    async def update(
        self, user_id: str, user_dto: UpdateUserDTO, agent_roles: list[Roles] = []
    ):
        if Roles.ADMIN in user_dto.roles and Roles.ADMIN not in agent_roles:
            raise HTTPException(
                detail='Você não tem permissão para tornar um usuário ADMIN.',
                status_code=status.HTTP_403_FORBIDDEN,
            )

        user_to_update = await self.find_by_id(user_id)

        if user_to_update.fl_google_user is False and user_dto.password is None:
            raise HTTPException(
                detail='Você precisa passar uma senha para um usuário de sistema.',
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        update_email_google_user = (
            user_to_update.fl_google_user is True
            and user_dto.email != user_to_update.email
        )

        if update_email_google_user:
            if user_dto.password is None:
                raise HTTPException(
                    detail='Você precisa inserir uma senha ao editar o email de um usuário google. A autenticação pelo google também não estará mais possivel.',
                    status_code=status.HTTP_400_BAD_REQUEST,
                )

            user_to_update.fl_google_user = False

        email_already_register = (
            await self.user_repository.find_by_email(user_dto.email, user_to_update.id)
            is not None
        )

        if email_already_register:
            raise HTTPException(
                detail='Usuário já cadastrado com esse email.',
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        user_to_update.update(user_dto)
        user_to_update = await self.user_repository.save(user_to_update)

        return user_to_update

    async def delete(self, user_id: str):
        user = await self.find_by_id(user_id)
        await self.user_repository.delete(user)
