from contextlib import asynccontextmanager
from typing import Optional

from attr import attrs, attrib

from application.infrastructure.configurations.models import Configuration
from application.infrastructure.database.models import HousingUnitsDBBaseModel
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine


@attrs
class AsyncDBEngine:
    async_engine = attrib(type=AsyncEngine)
    async_session = attrib(type=sessionmaker)
    async_scoped_session_factory = attrib(type=scoped_session)


class DatabaseEngineWrapper:
    ASYNC_DB_ENGINE: Optional[AsyncDBEngine] = None

    @classmethod
    def initialize(cls) -> None:
        config: Configuration = Configuration.initialize()

        if not cls.ASYNC_DB_ENGINE:
            async_engine = create_async_engine(url=config.postgresql_connection_uri, echo=True)
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

    @classmethod
    def get(cls) -> AsyncDBEngine:
        if not cls.ASYNC_DB_ENGINE:
            cls.initialize()

        return cls.ASYNC_DB_ENGINE

    @staticmethod
    async def create_database() -> None:
        async with DatabaseEngineWrapper.get().async_engine.begin() as engine_connection:
            await engine_connection.run_sync(HousingUnitsDBBaseModel.metadata.create_all)

    @staticmethod
    @asynccontextmanager
    async def get_session() -> AsyncSession:
        _scoped_session = DatabaseEngineWrapper.get().async_scoped_session_factory()
        try:
            yield _scoped_session
        except Exception as ex:
            await _scoped_session.rollback()
            raise ex
        finally:
            await _scoped_session.close()

# config: Configuration = Configuration.initialize()
# async_engine = create_async_engine(url=config.postgresql_connection_uri, echo=True)
# async_session = sessionmaker(
#     async_engine, class_=AsyncSession, expire_on_commit=False
# )
# async_scoped_session_factory: scoped_session = scoped_session(
#     session_factory=async_session
# )


# async def create_database() -> None:
#     async with async_engine.begin() as engine_connection:
#         await engine_connection.run_sync(HousingUnitsDBBaseModel.metadata.create_all)
#
#
# @asynccontextmanager
# async def get_session() -> AsyncSession:
#     _scoped_session = async_scoped_session_factory()
#     try:
#         yield _scoped_session
#     except Exception as ex:
#         await _scoped_session.rollback()
#         raise ex
#     finally:
#         await _scoped_session.close()
