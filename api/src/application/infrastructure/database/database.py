from contextlib import asynccontextmanager


from application.infrastructure.configurations.models import Configuration
from application.infrastructure.database.models import HousingUnitsDBBaseModel
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

config: Configuration = Configuration.initialize()
async_engine = create_async_engine(url=config.postgresql_connection_uri, echo=True)
async_session = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)
async_scoped_session_factory: scoped_session = scoped_session(
    session_factory=async_session
)


async def create_database() -> None:
    async with async_engine.begin() as engine_connection:
        await engine_connection.run_sync(HousingUnitsDBBaseModel.metadata.create_all)


@asynccontextmanager
async def get_session() -> AsyncSession:
    _scoped_session = async_scoped_session_factory()
    try:
        yield _scoped_session
    except Exception as ex:
        await _scoped_session.rollback()
        raise ex
    finally:
        await _scoped_session.close()
