from dependency_injector import containers, providers
from dependency_injector.providers import Factory

from application.infrastructure.configurations.models import Configuration
from application.infrastructure.database.container import DatabaseContainer
from application.infrastructure.loggers.loggers import HousingUnitsAppLoggerFactory
from application.users.repositories import UserRepository
from application.users.services import UserService


class UserContainer(containers.DeclarativeContainer):
    """
    User inversion of control Container.
    """

    wiring_config = containers.WiringConfiguration(modules=["..rest_api.users.controller"])

    config = Configuration.initialize()
    logger = HousingUnitsAppLoggerFactory.get()

    user_repository: Factory = providers.Factory(
        UserRepository,
        session_factory=DatabaseContainer.db_engine_wrapper.provided.session,
    )

    user_service = providers.Factory(
        UserService,
        user_repository=user_repository,
    )
