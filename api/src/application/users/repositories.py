from typing import Iterator

from application.users.models import User


class UserRepository:

    def __init__(self, session_factory: callable) -> None:
        self.session_factory = session_factory

    def get_all(self) -> Iterator[User]:
        with self.session_factory() as session:
            return session.query(User).all()

    def get_by_email(self, email: str) -> Iterator[User]:
        with self.session_factory() as session:
            return session.query(User).filter(User.email == email).first()
