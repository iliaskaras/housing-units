from typing import List

from sqlalchemy import delete
from sqlalchemy.engine import ChunkedIteratorResult
from sqlalchemy.future import select
from sqlalchemy.orm import FromStatement
from sqlalchemy.sql import Select

from application.housing_units.models import HousingUnit
from application.infrastructure.database.database import DatabaseEngineWrapper


class HousingUnitsRepository:

    def __init__(self, db_engine: DatabaseEngineWrapper = None):
        self.db_engine = db_engine

    async def get_by_uuid(self, uuid: str) -> HousingUnit:
        """
        Async call using the async session for retrieving a HousingUnit entry by uuid.

        :param uuid: The HousingUnit's uuid to retrieve.

        :return: The HousingUnit retrieved.
        """
        async with self.db_engine.get_async_session() as session:
            query: Select = select(HousingUnit).where(HousingUnit.uuid == uuid)
            results: ChunkedIteratorResult = await session.execute(query)
            return results.scalars().first()

    def truncate_table(self) -> None:
        """
        HousingUnit table truncate using the sync session.
        """
        with self.db_engine.get_session() as session:
            session.execute("TRUNCATE TABLE housingunits")
            session.commit()

    async def delete(
            self,
            uuid: str,
    ) -> HousingUnit:
        """
        Async call using the async session for deleting a HousingUnit by uuid.

        :param uuid: The HousingUnit's uuid to delete.

        :return: The HousingUnit deleted.
        """
        async with self.db_engine.get_async_session() as session:
            async with session.begin():
                stmt = (
                    delete(HousingUnit).where(HousingUnit.uuid == uuid)
                ).returning(HousingUnit)

                orm_stmt: FromStatement = (
                    select(HousingUnit).from_statement(stmt).execution_options(populate_existing=True)
                )

                return await session.execute(
                    orm_stmt,
                ).scalars().first()

    async def save(
            self,
            housing_unit: HousingUnit,
    ) -> HousingUnit:
        """
        Async call using the async session for saving a HousingUnit entry.

        :param housing_unit: The HousingUnit to save.

        :return: The saved HousingUnit.
        """

        async with self.db_engine.get_async_session() as session:
            async with session.begin():
                session.add(housing_unit)
                return housing_unit

    def bulk_save(
            self,
            housing_units: List[HousingUnit],
    ) -> None:
        """
        HousingUnit table bulk save operation using the sync session.

        :param housing_units: The HousingUnits to bulk save.
        """
        with self.db_engine.get_session() as session:
            with session.begin():
                session.add_all(housing_units)
