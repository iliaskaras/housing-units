from dependency_injector import containers, providers
from application.authentication.services import GetJWTService
from application.authentication.validators import JwtValidator
from application.infrastructure.configurations.models import Configuration


class AuthenticationContainer(containers.DeclarativeContainer):
    """
    Authentication inversion of control Container.
    """

    wiring_config = containers.WiringConfiguration(modules=["..rest_api.users.controllers"])

    config = Configuration.initialize()

    get_jwt_service = providers.Singleton(
        GetJWTService,
        jwt_validator=JwtValidator(),
        config=config
    )
