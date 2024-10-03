from fastapi import Depends
from dataclasses import dataclass
from sqlalchemy import select
from api.database import get_db, AsyncSession
from api.user.user_model import User
from api.utils.logger import ilogger


@dataclass
class UserRepository:
    db: AsyncSession = Depends(get_db)

    async def find_all(self) -> list[User]:
        query = select(User)

        result = await self.db.execute(query)
        return result.scalars().all()

    async def find_by_id(self, id: int) -> User | None:
        query = select(User).where(User.id == id)

        result = await self.db.execute(query)
        return result.scalars().first()

    async def find_by_email(self, email: str, id: int | None = None) -> User | None:
        query = select(User).where(User.email == email)

        if id is not None:
            query = query.where(User.id != id)

        result = await self.db.execute(query)
        return result.scalars().first()

    async def save(self, user: User):
        try:
            self.db.add(user)
            await self.db.commit()
            return user
        except Exception as err:
            ilogger.error(f'Houve um error ao salvar usuário: {err}')

    async def delete(self, user: User):
        try:
            await self.db.delete(user)
            await self.db.commit()
        except Exception as err:
            ilogger.error(f'Houve um error ao excluir usuário: {err}')
