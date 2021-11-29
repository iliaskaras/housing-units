from typing import Iterator

from application.authentication.errors import AuthenticationError
from application.authentication.models import JwtBody
from application.authentication.services import GetJWTService
from application.infrastructure.error.errors import InvalidArgumentError
from application.rest_api.authentication.schemas import AuthenticateJwtResponse
from application.users.models import User
from application.users.repositories import UserRepository


class LoginUserService:

    def __init__(
            self,
            user_repository: UserRepository,
            get_jwt_service: GetJWTService
    ) -> None:
        self._repository: UserRepository = user_repository
        self.get_jwt_service: GetJWTService = get_jwt_service

    async def apply(self, email: str = None, password: str = None) -> AuthenticateJwtResponse:
        """
        Authenticates the user and returns the jwt in case of success.

        :param email: The User email.
        :param password: The User password.

        :return: The encoded JWT token.

        :raises InvalidArgumentError: If email or password is not provided.
                AuthenticationError: If the user does not exist.
        """
        if email is None:
            raise InvalidArgumentError("The user email is not provided.")
        if password is None:
            raise InvalidArgumentError("The user password is not provided.")

        user: User = await self._repository.get_by_email(email)

        if user is None:
            raise AuthenticationError("The user does not exist.")

        return AuthenticateJwtResponse(
            access_token=self.get_jwt_service.apply(
                jwt_body=JwtBody(
                    user_id=user.email,
                    group=user.user_group.value
                )
            )
        )


class GetActiveUsersService:

    def __init__(self, user_repository: UserRepository) -> None:
        self._repository: UserRepository = user_repository

    async def apply(self) -> Iterator[User]:
        """
        Service for returning all the active users.

        :return: The active users.
        """
        return await self._repository.get_active_users()
