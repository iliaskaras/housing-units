from typing import Iterator

from sqlalchemy.future import select

from application.infrastructure.database.database import DatabaseEngineWrapper
from application.users.models import User


class UserRepository:

    def __init__(self, db_engine: DatabaseEngineWrapper = None):
        self.db_engine = db_engine

    async def get_all(self) -> Iterator[User]:
        async with self.db_engine.get_session() as session:
            result = await session.execute(select(User))
            users = result.scalars().all()
            return users

    async def get_by_email(self, email: str) -> Iterator[User]:
        async with self.db_engine.get_session() as session:
            return session.query(User).filter(User.email == email).first()
