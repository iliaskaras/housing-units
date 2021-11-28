from typing import Iterator

from application.users.models import User
from application.users.repositories import UserRepository


class UserService:

    def __init__(self, user_repository: UserRepository) -> None:
        self._repository: UserRepository = user_repository

    def get_users(self) -> Iterator[User]:
        return self._repository.get_all()
