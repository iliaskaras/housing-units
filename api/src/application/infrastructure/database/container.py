from logging import Logger

from dependency_injector import containers, providers

from application.infrastructure.configurations.models import Configuration
from application.infrastructure.database.database import DatabaseEngineWrapper
from application.infrastructure.loggers.loggers import HousingUnitsAppLoggerFactory


class DatabaseContainer(containers.DeclarativeContainer):
    """
    Database inversion of control Container.
    """

    config: Configuration = Configuration.initialize()
    logger: Logger = HousingUnitsAppLoggerFactory.get()

    db_engine_wrapper = providers.Singleton(
        DatabaseEngineWrapper,
        db_url=config.postgresql_connection_uri,
        logger=logger
    )
