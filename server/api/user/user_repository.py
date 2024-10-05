from fastapi import Depends
from dataclasses import dataclass
from sqlalchemy import select
from api.database import get_db, Session
from api.user.user_model import User
from api.utils.logger import ilogger


@dataclass
class UserRepository:
    db: Session = Depends(get_db)

    def find_all(self) -> list[User]:
        query = select(User)

        result = self.db.execute(query)
        return result.scalars().all()

    def find_by_id(self, id: int) -> User | None:
        query = select(User).where(User.id == id)

        result = self.db.execute(query)
        return result.scalars().first()

    def find_by_email(self, email: str, id: int | None = None) -> User | None:
        query = select(User).where(User.email == email)

        if id is not None:
            query = query.where(User.id != id)

        result = self.db.execute(query)
        return result.scalars().first()

    def save(self, user: User):
        try:
            self.db.add(user)
            self.db.commit()

            return user
        except Exception as err:
            ilogger.error(f'Houve um error ao salvar usuário: {err}')

    def delete(self, user: User):
        try:
            self.db.delete(user)
            self.db.commit()
        except Exception as err:
            ilogger.error(f'Houve um error ao excluir usuário: {err}')
