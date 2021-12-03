from typing import List, Optional

import pytest
import uuid
from sqlalchemy.future import select

from application.housing_units.models import HousingUnit
from application.housing_units.repositories import HousingUnitsRepository
from application.infrastructure.database.database import DatabaseEngineWrapper


class TestHousingUnitsRepository:

    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.housing_units_repository = HousingUnitsRepository(
            db_engine=DatabaseEngineWrapper()
        )

    @pytest.mark.parametrize(
        'street_name, borough, postcode, construction_type, num_units_min, num_units_max, '
        # Expected results.
        'expected_results',
        [
            # when_only_street_name_is_provided
            (
                    'street name test 1',  # street_name
                    None,  # borough
                    None,  # postcode
                    None,  # construction_type
                    None,  # num_units_min
                    None,  # num_units_max
                    [
                        HousingUnit(
                            project_id='project id 12',
                            street_name='street name test 1',
                            borough='Queens',
                            postcode=1,
                            reporting_construction_type='construction type test 1',
                            total_units=25
                        ),
                        HousingUnit(
                            project_id='project id 12',
                            street_name='street name test 1',
                            borough='Queens',
                            postcode=1,
                            reporting_construction_type='construction type test 1',
                            total_units=25
                        ),
                        HousingUnit(
                            project_id='project id 11',
                            street_name='street name test 1',
                            borough='Queens',
                            postcode=1,
                            reporting_construction_type='construction type test 1',
                            total_units=16
                        ),
                        HousingUnit(
                            project_id='project id 6',
                            street_name='street name test 1',
                            borough='Queens',
                            postcode=1,
                            reporting_construction_type='construction type test 1',
                            total_units=12
                        ),
                        HousingUnit(
                            project_id='project id 1',
                            street_name='street name test 1',
                            borough='Queens',
                            postcode=1,
                            reporting_construction_type='construction type test 1',
                            total_units=2
                        ),
                    ]
            ),
            # when_only_borough_is_provided
            (
                    None,  # street_name
                    'brooklyn',  # borough
                    None,  # postcode
                    None,  # construction_type
                    None,  # num_units_min
                    None,  # num_units_max
                    [
                        HousingUnit(
                            project_id='project id 7',
                            street_name='street name test 2',
                            borough='Brooklyn',
                            postcode=2,
                            reporting_construction_type='construction type test 2',
                            total_units=14
                        ),
                        HousingUnit(
                            project_id='project id 2',
                            street_name='street name test 2',
                            borough='Brooklyn',
                            postcode=2,
                            reporting_construction_type='construction type test 2',
                            total_units=4
                        ),
                    ]
            ),
            # when_only_postcode_is_provided
            (
                    None,  # street_name
                    None,  # borough
                    3,  # postcode
                    None,  # construction_type
                    None,  # num_units_min
                    None,  # num_units_max
                    [
                        HousingUnit(
                            project_id='project id 8',
                            street_name='street name test 3',
                            borough='Staten Island',
                            postcode=3,
                            reporting_construction_type='construction type test 3',
                            total_units=16
                        ),
                        HousingUnit(
                            project_id='project id 3',
                            street_name='street name test 3',
                            borough='Staten Island',
                            postcode=3,
                            reporting_construction_type='construction type test 3',
                            total_units=6
                        ),
                    ]
            ),
            # when_only_construction_type_is_provided
            (
                    None,  # street_name
                    None,  # borough
                    None,  # postcode
                    'construction type test 4',  # construction_type
                    None,  # num_units_min
                    None,  # num_units_max
                    [
                        HousingUnit(
                            project_id='project id 9',
                            street_name='street name test 4',
                            borough='Manhattan',
                            postcode=4,
                            reporting_construction_type='construction type test 4',
                            total_units=18
                        ),
                        HousingUnit(
                            project_id='project id 4',
                            street_name='street name test 4',
                            borough='Manhattan',
                            postcode=4,
                            reporting_construction_type='construction type test 4',
                            total_units=8
                        ),
                    ]
            ),
            # when_only_num_units_max_is_provided
            (
                    None,  # street_name
                    None,  # borough
                    None,  # postcode
                    None,  # construction_type
                    None,  # num_units_min
                    10,  # num_units_max
                    [
                        HousingUnit(
                            project_id='project id 1',
                            street_name='street name test 1',
                            borough='Queens',
                            postcode=1,
                            reporting_construction_type='construction type test 1',
                            total_units=2
                        ),
                        HousingUnit(
                            project_id='project id 2',
                            street_name='street name test 2',
                            borough='Brooklyn',
                            postcode=2,
                            reporting_construction_type='construction type test 2',
                            total_units=4
                        ),
                        HousingUnit(
                            project_id='project id 3',
                            street_name='street name test 3',
                            borough='Staten Island',
                            postcode=3,
                            reporting_construction_type='construction type test 3',
                            total_units=6
                        ),
                        HousingUnit(
                            project_id='project id 4',
                            street_name='street name test 4',
                            borough='Manhattan',
                            postcode=4,
                            reporting_construction_type='construction type test 4',
                            total_units=8
                        ),
                        HousingUnit(
                            project_id='project id 5',
                            street_name='street name test 5',
                            borough='Bronx',
                            postcode=5,
                            reporting_construction_type='construction type test 5',
                            total_units=10
                        ),
                    ]
            ),
            # when_only_num_units_min_is_provided
            (
                    None,  # street_name
                    None,  # borough
                    None,  # postcode
                    None,  # construction_type
                    10,  # num_units_min
                    None,  # num_units_max
                    [
                        HousingUnit(
                            project_id='project id 5',
                            street_name='street name test 5',
                            borough='Bronx',
                            postcode=5,
                            reporting_construction_type='construction type test 5',
                            total_units=10
                        ),
                        HousingUnit(
                            project_id='project id 6',
                            street_name='street name test 1',
                            borough='Queens',
                            postcode=1,
                            reporting_construction_type='construction type test 1',
                            total_units=12
                        ),
                        HousingUnit(
                            project_id='project id 7',
                            street_name='street name test 2',
                            borough='Brooklyn',
                            postcode=2,
                            reporting_construction_type='construction type test 2',
                            total_units=14
                        ),
                        HousingUnit(
                            project_id='project id 8',
                            street_name='street name test 3',
                            borough='Staten Island',
                            postcode=3,
                            reporting_construction_type='construction type test 3',
                            total_units=16
                        ),
                        HousingUnit(
                            project_id='project id 9',
                            street_name='street name test 4',
                            borough='Manhattan',
                            postcode=4,
                            reporting_construction_type='construction type test 4',
                            total_units=18
                        ),
                        HousingUnit(
                            project_id='project id 10',
                            street_name='street name test 5',
                            borough='Bronx',
                            postcode=5,
                            reporting_construction_type='construction type test 5',
                            total_units=20
                        ),
                        HousingUnit(
                            project_id='project id 11',
                            street_name='street name test 1',
                            borough='Queens',
                            postcode=1,
                            reporting_construction_type='construction type test 1',
                            total_units=16
                        ),
                        HousingUnit(
                            project_id='project id 12',
                            street_name='street name test 1',
                            borough='Queens',
                            postcode=1,
                            reporting_construction_type='construction type test 1',
                            total_units=25
                        ),
                        HousingUnit(
                            project_id='project id 12',
                            street_name='street name test 1',
                            borough='Queens',
                            postcode=1,
                            reporting_construction_type='construction type test 1',
                            total_units=25
                        ),
                    ]
            ),
            # when_both_num_units_min_and_max_are_provided
            (
                    None,  # street_name
                    None,  # borough
                    None,  # postcode
                    None,  # construction_type
                    10,  # num_units_min
                    16,  # num_units_max
                    [
                        HousingUnit(
                            project_id='project id 5',
                            street_name='street name test 5',
                            borough='Bronx',
                            postcode=5,
                            reporting_construction_type='construction type test 5',
                            total_units=10
                        ),
                        HousingUnit(
                            project_id='project id 6',
                            street_name='street name test 1',
                            borough='Queens',
                            postcode=1,
                            reporting_construction_type='construction type test 1',
                            total_units=12
                        ),
                        HousingUnit(
                            project_id='project id 7',
                            street_name='street name test 2',
                            borough='Brooklyn',
                            postcode=2,
                            reporting_construction_type='construction type test 2',
                            total_units=14
                        ),
                        HousingUnit(
                            project_id='project id 11',
                            street_name='street name test 1',
                            borough='Queens',
                            postcode=1,
                            reporting_construction_type='construction type test 1',
                            total_units=16
                        ),
                        HousingUnit(
                            project_id='project id 8',
                            street_name='street name test 3',
                            borough='Staten Island',
                            postcode=3,
                            reporting_construction_type='construction type test 3',
                            total_units=16
                        ),
                    ]
            ),
            # when_combination_of_all_fields_are_provided
            (
                    'street name test 1',  # street_name
                    'Queens',  # borough
                    1,  # postcode
                    'construction type test 1',  # construction_type
                    10,  # num_units_min
                    16,  # num_units_max
                    [
                        HousingUnit(
                            project_id='project id 11',
                            street_name='street name test 1',
                            borough='Queens',
                            postcode=1,
                            reporting_construction_type='construction type test 1',
                            total_units=16
                        ),
                        HousingUnit(
                            project_id='project id 6',
                            street_name='street name test 1',
                            borough='Queens',
                            postcode=1,
                            reporting_construction_type='construction type test 1',
                            total_units=12
                        ),
                    ]
            ),
            # when_combination_of_all_fields_are_provided_and_nothing_is_found
            (
                    'street name test 1',  # street_name
                    'Queens',  # borough
                    1,  # postcode
                    'construction type test 1',  # construction_type
                    26,  # num_units_min
                    30,  # num_units_max
                    []
            ),
            # when_num_units_min_is_greater_than_num_units_max_that_there_arent_results
            (
                    'street name test 1',  # street_name
                    'Queens',  # borough
                    1,  # postcode
                    'construction type test 1',  # construction_type
                    10,  # num_units_min
                    5,  # num_units_max
                    []
            ),
        ]
    )
    @pytest.mark.asyncio
    async def test_filter(
            self,
            populate_housing_units,
            street_name: Optional[str],
            borough: Optional[str],
            postcode: Optional[int],
            construction_type: Optional[str],
            num_units_min: Optional[int],
            num_units_max: Optional[int],
            expected_results: Optional[List[HousingUnit]]
    ) -> None:
        results: List[HousingUnit] = await self.housing_units_repository.filter(
            street_name=street_name,
            borough=borough,
            postcode=postcode,
            construction_type=construction_type,
            num_units_min=num_units_min,
            num_units_max=num_units_max,
        )

        assert len(expected_results) == len(results)
        for housing_unit_result, expected_housing_unit in zip(results, expected_results):
            assert housing_unit_result == expected_housing_unit

    @pytest.mark.asyncio
    async def test_save(self, populate_housing_units, stub_housing_units) -> None:
        await self.housing_units_repository.save(
            HousingUnit(
                project_id='project id 6',
                street_name='street name test 1',
                borough='Queens',
                postcode=1,
                reporting_construction_type='construction type test 1',
                total_units=12
            )
        )

        async with self.housing_units_repository.db_engine.get_async_session() as session:
            query = select(HousingUnit)
            housing_units = await session.execute(query)
            after_save_total_housing_units = housing_units.scalars().all()

        assert len(after_save_total_housing_units) == len(stub_housing_units) + 1

    def test_bulk_save(self, populate_housing_units, stub_housing_units) -> None:
        self.housing_units_repository.bulk_save(
            [
                HousingUnit(
                    project_id='project id 6',
                    street_name='street name test 1',
                    borough='Queens',
                    postcode=1,
                    reporting_construction_type='construction type test 1',
                    total_units=12
                ),
                HousingUnit(
                    project_id='project id 7',
                    street_name='street name test 1',
                    borough='Queens',
                    postcode=1,
                    reporting_construction_type='construction type test 1',
                    total_units=12
                ),
            ]
        )

        with self.housing_units_repository.db_engine.get_session() as session:
            query = select(HousingUnit)
            housing_units = session.execute(query)
            after_save_total_housing_units = housing_units.scalars().all()

        assert len(after_save_total_housing_units) == len(stub_housing_units) + 2

    @pytest.mark.asyncio
    async def test_delete(self, populate_housing_units, stub_housing_units) -> None:
        async with self.housing_units_repository.db_engine.get_async_session() as session:
            query = select(HousingUnit)
            housing_units = await session.execute(query)
            housing_unit_to_delete = housing_units.scalars().first()

        await self.housing_units_repository.delete(uuid=str(housing_unit_to_delete.uuid))

        async with self.housing_units_repository.db_engine.get_async_session() as session:
            query = select(HousingUnit)
            housing_units = await session.execute(query)
            after_delete_total_housing_units = housing_units.scalars().all()

        assert len(after_delete_total_housing_units) == len(stub_housing_units) - 1

    @pytest.mark.asyncio
    async def test_get_by_uuid(self, populate_housing_units) -> None:
        async with self.housing_units_repository.db_engine.get_async_session() as session:
            query = select(HousingUnit)
            housing_units = await session.execute(query)
            housing_unit_to_retrieve = housing_units.scalars().first()

        returned_housing_unit: HousingUnit = await self.housing_units_repository.get_by_uuid(
            uuid=str(housing_unit_to_retrieve.uuid)
        )

        assert returned_housing_unit == housing_unit_to_retrieve

    @pytest.mark.asyncio
    async def test_get_by_uuid_returns_none_when_entry_does_not_exist(
            self, populate_housing_units
    ) -> None:
        returned_housing_unit: HousingUnit = await self.housing_units_repository.get_by_uuid(
            uuid=str(uuid.uuid4())
        )

        assert returned_housing_unit is None
