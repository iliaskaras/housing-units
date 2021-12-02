import os

from application.infrastructure.configurations.enums import APIEnvironment
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
            async_postgresql_connection_uri: str,
            postgresql_connection_uri: str,
            celery_broker_url: str,
            celery_result_backend: str,
            secret: str,
            socrata_app_token: str,
            algorithm: str = "HS256",
            debug: bool = False,
            create_db_tables: bool = False,
    ):
        if not postgresql_connection_uri:
            raise InvalidArgumentError("The PostGreSQL connection uri is required.")
        if not async_postgresql_connection_uri:
            raise InvalidArgumentError("The Async PostGreSQL connection uri is required.")
        if not celery_broker_url:
            raise InvalidArgumentError("The Celery Broker url is required.")
        if not celery_result_backend:
            raise InvalidArgumentError("The Celery Result backend is required.")
        if not secret:
            raise InvalidArgumentError("The secret is required.")
        if not socrata_app_token:
            raise InvalidArgumentError("The socrata app token is required.")
        if not algorithm:
            raise InvalidArgumentError("The algorithm is required.")

        self.postgresql_connection_uri = postgresql_connection_uri
        self.async_postgresql_connection_uri = async_postgresql_connection_uri
        self.celery_broker_url = celery_broker_url
        self.celery_result_backend = celery_result_backend
        self.secret = secret
        self.socrata_app_token = socrata_app_token
        self.algorithm = algorithm
        self.debug = debug
        self.create_db_tables = create_db_tables

    @classmethod
    def initialize(cls) -> "Configuration":
        """
        Initializes the Application Configuration, or returns it in case the initialization already run.

        :return The Configuration instance.

        :raises InvalidArgumentError: If the provided environment is not one of the supported ones.
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
        Returns the already initialized application configuration instance, if it initialized already,
        if not initializes it as well.

        :return: The initialized configuration instance.
        """

        if not cls.INSTANCE:
            cls.initialize()

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
            async_postgresql_connection_uri=os.getenv("ASYNC_POSTGRESQL_CONNECTION_URI"),
            celery_broker_url=os.getenv("CELERY_BROKER_URL"),
            celery_result_backend=os.getenv("CELERY_RESULT_BACKEND"),
            secret=os.getenv("SECRET"),
            socrata_app_token=os.getenv("SOCRATA_APP_TOKEN"),
            algorithm=os.getenv("ALGORITHM", "HS256"),
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
            async_postgresql_connection_uri='',
            celery_broker_url="redis://localhost:6379",
            celery_result_backend="redis://localhost:6379",
            secret=os.getenv("SECRET"),
            socrata_app_token=os.getenv("SOCRATA_APP_TOKEN"),
            algorithm=os.getenv("ALGORITHM", "HS256"),
            debug=True,
            create_db_tables=True,
        )
