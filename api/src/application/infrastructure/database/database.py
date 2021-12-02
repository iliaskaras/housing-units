from contextlib import asynccontextmanager, contextmanager
from typing import Optional

from attr import attrs, attrib
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from application.infrastructure.configurations.models import Configuration
from application.infrastructure.database.models import HousingUnitsDBBaseModel
from sqlalchemy.orm import sessionmaker, scoped_session, Session
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine


@attrs
class AsyncDBEngine:
    async_engine = attrib(type=AsyncEngine)
    async_session = attrib(type=sessionmaker)
    async_scoped_session_factory = attrib(type=scoped_session)


@attrs
class DBEngine:
    engine = attrib(type=Engine)
    session = attrib(type=sessionmaker)
    scoped_session_factory = attrib(type=scoped_session)


class DatabaseEngineWrapper:
    """
    The Singleton DB Engine wrapper containing the applications async and sync engines and session makers.
    """
    ASYNC_DB_ENGINE: Optional[AsyncDBEngine] = None
    DB_ENGINE: Optional[DBEngine] = None

    @classmethod
    def initialize(cls) -> None:
        """
        Initializes the async and sync db engines with their respective session makers.
        """
        config: Configuration = Configuration.initialize()

        if not cls.ASYNC_DB_ENGINE:
            async_engine = create_async_engine(url=config.async_postgresql_connection_uri, echo=True)
            async_session = sessionmaker(
                async_engine, class_=AsyncSession, expire_on_commit=False
            )
            cls.ASYNC_DB_ENGINE = AsyncDBEngine(
                async_engine=async_engine,
                async_session=async_session,
                async_scoped_session_factory=scoped_session(
                    session_factory=async_session
                )
            )
        if not cls.DB_ENGINE:
            engine = create_engine(
                url=config.postgresql_connection_uri,
                echo=True
            )
            session = sessionmaker(engine, expire_on_commit=False)
            cls.DB_ENGINE = DBEngine(
                engine=engine,
                session=session,
                scoped_session_factory=scoped_session(
                    session_factory=session
                )
            )

    @classmethod
    def get_async_engine(cls) -> AsyncDBEngine:
        if not cls.ASYNC_DB_ENGINE:
            cls.initialize()

        return cls.ASYNC_DB_ENGINE

    @classmethod
    def get_engine(cls) -> DBEngine:
        if not cls.DB_ENGINE:
            cls.initialize()

        return cls.DB_ENGINE

    @staticmethod
    async def create_database() -> None:
        async with DatabaseEngineWrapper.get_async_engine().async_engine.begin() as engine_connection:
            await engine_connection.run_sync(HousingUnitsDBBaseModel.metadata.create_all)

    @staticmethod
    @asynccontextmanager
    async def get_async_session() -> AsyncSession:
        _scoped_session = DatabaseEngineWrapper.get_async_engine().async_scoped_session_factory()
        try:
            yield _scoped_session
        except Exception as ex:
            await _scoped_session.rollback()
            raise ex
        finally:
            await _scoped_session.close()

    @staticmethod
    @contextmanager
    def get_session() -> Session:
        _scoped_session = DatabaseEngineWrapper.get_engine().scoped_session_factory()
        try:
            yield _scoped_session
        except Exception as ex:
            _scoped_session.rollback()
            raise ex
        finally:
            _scoped_session.close()
