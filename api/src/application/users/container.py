from dependency_injector import containers, providers
from dependency_injector.providers import Singleton

from application.authentication.container import AuthenticationContainer
from application.infrastructure.database.database import DatabaseEngineWrapper
from application.users.repositories import UserRepository
from application.users.services import LoginUserService, GetActiveUsersService


class UserContainer(containers.DeclarativeContainer):
    """
    User inversion of control Container.
    """

    wiring_config = containers.WiringConfiguration(
        modules=[
            "..rest_api.users.controllers",
            "..rest_api.authentication.controllers",
        ]
    )

    user_repository: Singleton = providers.Singleton(
        UserRepository,
        db_engine=DatabaseEngineWrapper
    )

    get_active_users_service: Singleton = providers.Singleton(
        GetActiveUsersService,
        user_repository=user_repository,
    )

    login_user_service: Singleton = providers.Singleton(
        LoginUserService,
        user_repository=user_repository,
        get_jwt_service=AuthenticationContainer.get_jwt_service.provided
    )
