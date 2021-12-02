from fastapi import FastAPI

from application.authentication.container import AuthenticationContainer
from application.housing_units.container import HousingUnitsContainer
from application.infrastructure.configurations.models import Configuration
from application.infrastructure.error.errors import InvalidArgumentError
from application.infrastructure.loggers.loggers import HousingUnitsAppLoggerFactory
from application.rest_api.users import controllers as user_route
from application.rest_api.authentication import controllers as authenticate_route
from application.rest_api.housing_units import controllers as housing_units_route
from application.rest_api.task_status import controllers as task_status_route
from application.users.container import UserContainer


def init_application_containers() -> None:
    AuthenticationContainer()
    UserContainer()
    HousingUnitsContainer()


def init_application_routes(rest_api: FastAPI) -> None:
    rest_api.include_router(user_route.router)
    rest_api.include_router(authenticate_route.router)
    rest_api.include_router(housing_units_route.router)
    rest_api.include_router(task_status_route.router)


def create_housing_units_app(name: str) -> FastAPI:
    """
    The FastAPI Application Factory for the Housing Units application.
    Initializes and returns the Housing Units FastAPI application.

    :param name: The name of the FastAPI application.

    @return: The Housing Units FastAPI application.
    """
    if not name:
        raise InvalidArgumentError("The application name is required.")

    # Initialize the application logger instance.
    HousingUnitsAppLoggerFactory.initialize()
    logger = HousingUnitsAppLoggerFactory.get()

    # Initialize the configuration instance.
    Configuration.initialize()

    # Create the FastAPI application.
    rest_api = FastAPI(name=name)

    # Initialize Application Containers.
    init_application_containers()

    # Initialize Rest API Routes.
    init_application_routes(rest_api=rest_api)

    logger.info("Housing Units REST API started.")

    return rest_api
