from typing import List, Optional

from sqlalchemy import delete, and_
from sqlalchemy.engine import ChunkedIteratorResult
from sqlalchemy.future import select
from sqlalchemy.orm import FromStatement
from sqlalchemy.sql import Select
from sqlalchemy.sql.elements import BinaryExpression

from application.housing_units.column_mappings import UNIQUE_BOROUGH_MAPS
from application.housing_units.models import HousingUnit
from application.infrastructure.database.database import DatabaseEngineWrapper


class HousingUnitsRepository:

    def __init__(self, db_engine: DatabaseEngineWrapper = None):
        self.db_engine = db_engine

    async def filter(
            self,
            street_name: Optional[str] = None,
            borough: Optional[str] = None,
            postcode: Optional[int] = None,
            construction_type: Optional[str] = None,
            num_units_min: Optional[int] = None,
            num_units_max: Optional[int] = None,
    ) -> Optional[List[HousingUnit]]:
        """
        Async call using the async session for filtering the HousingUnits based on the provided filtering fields.

        :param street_name: The Housing Unit street name.
        :param borough: The Housing Unit borough.
        :param postcode: The Housing Unit postcode.
        :param construction_type: The Housing Unit construction type.
        :param num_units_min: The Housing Unit num_units_min.
        :param num_units_max: The Housing Unit num_units_max.

        :return: The HousingUnits found from the filtering.
        """
        async with self.db_engine.get_async_session() as session:
            filters: List[BinaryExpression] = []
            if street_name:
                filters.append(HousingUnit.street_name == street_name)
            if borough:
                filters.append(HousingUnit.borough == UNIQUE_BOROUGH_MAPS.get(borough.lower()))
            if postcode:
                filters.append(HousingUnit.postcode == postcode)
            if construction_type:
                filters.append(HousingUnit.reporting_construction_type == construction_type)
            if num_units_min is not None:
                filters.append(HousingUnit.total_units >= num_units_min)
            if num_units_max is not None:
                filters.append(HousingUnit.total_units <= num_units_max)

            query: Select = select(HousingUnit).where(
                and_(*filters)
            )
            results: ChunkedIteratorResult = await session.execute(query)
            return results.scalars().all()

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

                deleted_housing_unit_result: ChunkedIteratorResult = await session.execute(
                    orm_stmt,
                )
            return deleted_housing_unit_result.scalars().all()

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
