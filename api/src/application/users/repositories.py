from typing import Iterator

from sqlalchemy.future import select

from application.infrastructure.database.database import get_session
from application.users.models import User


class UserRepository:

    async def get_all(self) -> Iterator[User]:
        async with get_session() as session:
            result = await session.execute(select(User))
            users = result.scalars().all()
            return users

    async def get_by_email(self, email: str) -> Iterator[User]:
        async with get_session() as session:
            return session.query(User).filter(User.email == email).first()
