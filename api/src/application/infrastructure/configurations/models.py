import os

from application.infrastructure.configurations.enums import APIEnvironment
from application.infrastructure.configurations.errors import ConfigurationNotInitializedError
from application.infrastructure.error.errors import InvalidArgumentError
from application.infrastructure.loggers.loggers import HousingUnitsAppLoggerFactory

API_ENVIRONMENT = "HOUSING_UNITS_API_ENVIRONMENT"

logger = HousingUnitsAppLoggerFactory.get()


class Configuration:
    """
    The Application Configuration which is initialized at the application start up. Is singleton and is being
    used during the whole application lifecycle.
    """
    INSTANCE: "Configuration" = None

    def __init__(
            self,
            postgresql_connection_uri: str,
            celery_broker_url: str,
            celery_result_backend: str,
            debug: bool = False,
            create_db_tables: bool = False,
    ):
        if not postgresql_connection_uri:
            raise InvalidArgumentError("The PostGreSQL connection uri is required.")
        if not celery_broker_url:
            raise InvalidArgumentError("The Celery Broker url is required.")
        if not celery_result_backend:
            raise InvalidArgumentError("The Celery Result backend is required.")

        self.postgresql_connection_uri = postgresql_connection_uri
        self.celery_broker_url = celery_broker_url
        self.celery_result_backend = celery_result_backend
        self.debug = debug
        self.create_db_tables = create_db_tables

    @classmethod
    def initialize(cls) -> "Configuration":
        """
        Initializes the Application Configuration, or returns it in case the initialization already run.

        :return The Configuration instance.
        """
        if cls.INSTANCE:
            return cls.INSTANCE

        environment: str = os.getenv(API_ENVIRONMENT, None)
        if environment not in APIEnvironment.values():
            raise InvalidArgumentError(
                'Not supported api environment {0}, Choose a supported application environment, available: {1}'.format(
                    API_ENVIRONMENT, APIEnvironment.values()
                )
            )

        if environment == APIEnvironment.local.value:
            cls.INSTANCE = Configuration._initialize_local_configuration()
        elif environment == APIEnvironment.test.value:
            cls.INSTANCE = Configuration._initialize_test_configuration()

        return cls.INSTANCE

    @classmethod
    def get(cls) -> "Configuration":
        """
        Returns the already initialized application configuration instance.

        :return: The initialized configuration instance.

        :raises ConfigurationNotInitializedError: If the configuration has not been initialized.
        """

        if not cls.INSTANCE:
            raise ConfigurationNotInitializedError("Configuration has not been initialized.")

        return cls.INSTANCE

    @staticmethod
    def _initialize_local_configuration() -> "Configuration":
        """
        Initializes and returns a local configuration instance.

        :return: The local configuration instance.
        """
        logger.info("Initializing Housing Units API local configurations.")

        return Configuration(
            postgresql_connection_uri=os.getenv("POSTGRESQL_CONNECTION_URI"),
            celery_broker_url=os.getenv("CELERY_BROKER_URL"),
            celery_result_backend=os.getenv("CELERY_RESULT_BACKEND"),
            debug=bool(int(os.getenv("DEBUG", "0"))),
            create_db_tables=bool(int(os.getenv("CREATE_DB_TABLES", "0"))),
        )

    @staticmethod
    def _initialize_test_configuration() -> "Configuration":
        """
        Initializes and returns a test configuration instance.

        :return: The test configuration instance.
        """
        logger.info("Initializing Housing Units API test configurations.")

        return Configuration(
            postgresql_connection_uri='',
            celery_broker_url="redis://localhost:6379",
            celery_result_backend="redis://localhost:6379",
            debug=True,
            create_db_tables=True,
        )
