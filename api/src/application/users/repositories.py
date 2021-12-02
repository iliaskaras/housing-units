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
        """
        Async call using the async session for retrieving the active users.

        :return: The active Users.
        """
        async with self.db_engine.get_async_session() as session:
            query: Select = select(User).where(User.is_active == True)
            results: ChunkedIteratorResult = await session.execute(query)
            users = results.scalars().all()
            return users

    async def get_by_email(self, email: str) -> User:
        """
        Async call using the async session for retrieving an active User by email.

        :return: The active User.
        """
        async with self.db_engine.get_async_session() as session:
            query: Select = select(User).where(User.email == email, User.is_active == True)
            results: ChunkedIteratorResult = await session.execute(query)
            user = results.scalars().first()
            return user
