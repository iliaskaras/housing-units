from typing import Iterator

from sqlalchemy.engine import ChunkedIteratorResult
from sqlalchemy.future import select
from sqlalchemy.sql import Select

from application.infrastructure.database.database import DatabaseEngineWrapper
from application.users.models import User


class UserRepository:

    def __init__(self, db_engine: DatabaseEngineWrapper = None):
        self.db_engine = db_engine

    async def get_active_users(self) -> Iterator[User]:
        async with self.db_engine.get_session() as session:
            query: Select = select(User).where(User.is_active == True)
            results: ChunkedIteratorResult = await session.execute(query)
            users = results.scalars().all()
            return users

    async def get_by_email(self, email: str) -> User:
        async with self.db_engine.get_session() as session:
            query: Select = select(User).where(User.email == email)
            results: ChunkedIteratorResult = await session.execute(query)
            user = results.scalars().first()
            return user
