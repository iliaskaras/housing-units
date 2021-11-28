from contextlib import contextmanager
from logging import Logger
from typing import ContextManager

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, scoped_session, Session

from application.infrastructure.configurations.models import Configuration
from application.infrastructure.database.models import HousingUnitsDBBaseModel
from application.infrastructure.error.errors import NoneArgumentError


class DatabaseEngineWrapper:

    def __init__(
            self,
            db_url: str,
            echo: bool = False,
            logger: Logger = None
    ) -> None:
        """
        Application Database initialization using the database uri.
        Responsible for wrapping the Database Engine and its session maker factory.
        """
        logger.info("Initializing database engine wrapper.")

        if not db_url:
            raise NoneArgumentError('The database url is not provided.')

        self._engine: Engine = create_engine(url=db_url, echo=echo)
        self._session_maker_factory: sessionmaker = sessionmaker(bind=self._engine, autocommit=True, autoflush=False)
        self._scoped_session_factory: scoped_session = scoped_session(session_factory=self._session_maker_factory)
        self._logger: Logger = logger

    @staticmethod
    def create_database(config: Configuration) -> None:
        HousingUnitsDBBaseModel.metadata.create_all(create_engine(url=config.postgresql_connection_uri, echo=True))

    @contextmanager
    def session(self) -> ContextManager[Session]:
        """
        Session context manager, responsible for:
        - Session initialization
        - Transaction rollback in case of raised exception
        - Always closing the session

        :return:
        """
        _scoped_session = self._scoped_session_factory()
        try:
            yield _scoped_session
        except Exception as ex:
            self._logger.info("Rolling back the session during the following raised exception: {}.".format(ex))
            _scoped_session.rollback()
            raise ex
        finally:
            _scoped_session.close()
