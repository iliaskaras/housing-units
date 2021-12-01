from typing import List

from sqlalchemy import delete
from sqlalchemy.engine import ChunkedIteratorResult
from sqlalchemy.future import select
from sqlalchemy.orm import FromStatement
from sqlalchemy.sql import Select

from application.housing_units.models import HBDBuilding
from application.infrastructure.database.database import DatabaseEngineWrapper
from application.infrastructure.error.errors import InvalidArgumentError


class HBDBuildingRepository:

    def __init__(self, db_engine: DatabaseEngineWrapper = None):
        self.db_engine = db_engine

    async def get_by_uuid(self, uuid: str) -> HBDBuilding:
        async with self.db_engine.get_session() as session:
            query: Select = select(HBDBuilding).where(HBDBuilding.uuid == uuid)
            results: ChunkedIteratorResult = await session.execute(query)
            hbd_building = results.scalars().first()
            return hbd_building

    async def truncate_table(self):
        async with self.db_engine.get_session() as session:
            await session.execute("TRUNCATE TABLE hbdbuildings")
            await session.commit()

    async def delete(
            self,
            uuid: str,
    ) -> HBDBuilding:
        if not uuid:
            raise InvalidArgumentError('The id is not provided.')

        async with self.db_engine.get_session() as session:
            async with session.begin():
                stmt = (
                    delete(HBDBuilding).where(HBDBuilding.uuid == uuid)
                ).returning(HBDBuilding)

                orm_stmt: FromStatement = (
                    select(HBDBuilding).from_statement(stmt).execution_options(populate_existing=True)
                )

                return await session.execute(
                    orm_stmt,
                ).scalars().first()

    async def save(
            self,
            hbd_building: HBDBuilding,
    ) -> HBDBuilding:
        if not hbd_building:
            raise InvalidArgumentError('HBDBuilding is not provided.')

        async with self.db_engine.get_session() as session:
            async with session.begin():

                session.add(hbd_building)
                return hbd_building

    async def bulk_save(
            self,
            hbd_buildings: List[HBDBuilding],
    ) -> List[HBDBuilding]:
        if not hbd_buildings:
            raise InvalidArgumentError('List of HBDBuildings is not provided.')

        async with self.db_engine.get_session() as session:
            async with session.begin():
                session.add_all(hbd_buildings)

        return hbd_buildings
