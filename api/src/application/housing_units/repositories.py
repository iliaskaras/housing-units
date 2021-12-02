from typing import List

from sqlalchemy import delete
from sqlalchemy.engine import ChunkedIteratorResult
from sqlalchemy.future import select
from sqlalchemy.orm import FromStatement
from sqlalchemy.sql import Select

from application.housing_units.models import HBDBuilding
from application.infrastructure.database.database import DatabaseEngineWrapper


class HBDBuildingRepository:

    def __init__(self, db_engine: DatabaseEngineWrapper = None):
        self.db_engine = db_engine

    async def get_by_uuid(self, uuid: str) -> HBDBuilding:
        """
        Async call using the async session for retrieving a HBDBuilding entry by uuid.

        :param uuid: The HBDBuilding's uuid to retrieve.

        :return: The HBDBuilding retrieved.
        """
        async with self.db_engine.get_async_session() as session:
            query: Select = select(HBDBuilding).where(HBDBuilding.uuid == uuid)
            results: ChunkedIteratorResult = await session.execute(query)
            hbd_building = results.scalars().first()
            return hbd_building

    def truncate_table(self) -> None:
        """
        HBDBuilding table truncate using the sync session.
        """
        with self.db_engine.get_session() as session:
            session.execute("TRUNCATE TABLE hbdbuildings")
            session.commit()

    async def delete(
            self,
            uuid: str,
    ) -> HBDBuilding:
        """
        Async call using the async session for deleting a HBDBuilding by uuid.

        :param uuid: The HBDBuilding's uuid to delete.

        :return: The HBDBuilding deleted.
        """
        async with self.db_engine.get_async_session() as session:
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
        """
        Async call using the async session for saving a HBDBuilding entry.

        :param hbd_building: The HBDBuilding to save.

        :return: The saved HBDBuilding.
        """

        async with self.db_engine.get_async_session() as session:
            async with session.begin():
                session.add(hbd_building)
                return hbd_building

    def bulk_save(
            self,
            hbd_buildings: List[HBDBuilding],
    ) -> None:
        """
        HBDBuilding table bulk save operation using the sync session.

        :param hbd_buildings: The HBDBuildings to bulk save.
        """
        with self.db_engine.get_session() as session:
            with session.begin():
                session.add_all(hbd_buildings)
