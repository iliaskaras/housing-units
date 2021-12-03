from typing import Optional
from unittest import mock
from unittest.mock import MagicMock, AsyncMock

import pytest
from celery.result import AsyncResult

from application.housing_units.models import HousingUnit
from application.infrastructure.error.errors import InvalidArgumentError
from application.rest_api.housing_units.errors import InvalidNumUnitsError
from application.rest_api.housing_units.schemas import FilterHousingUnits, HousingUnitPostRequestBody
from application.rest_api.housing_units.services import FilterHousingUnitsService, HousingUnitsDataIngestionService, \
    RetrieveHousingUnitService, CreateHousingUnitService
from application.rest_api.task_status.schemas import TaskStatus
from application.task_status.services import GetTaskStatusReportService


class TestHousingUnitsDataIngestionService:

    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.housing_units_data_ingestion_service = HousingUnitsDataIngestionService(
            get_task_status_report_service=GetTaskStatusReportService()
        )

    @pytest.mark.asyncio
    async def test_apply_raise_error_when_hbd_dataset_id_is_not_provided(self) -> None:
        expected_error: InvalidArgumentError = InvalidArgumentError("The HBD dataset id is not provided.")

        with pytest.raises(InvalidArgumentError) as ex:
            await self.housing_units_data_ingestion_service.apply(
                hbd_dataset_id=None,
            )

        assert ex.value.args == expected_error.args
        assert ex.value.error_type == expected_error.error_type
        assert ex.value.message == expected_error.message

    @pytest.mark.parametrize(
        # Service input.
        'hbd_dataset_id, reset_table, '
        # Expected response.
        'expected_response',
        [
            (
                    'hbd-dataset-test',  # hbd_dataset_id
                    True,  # reset_table
                    TaskStatus(
                        task_id='3f6bf0e4-ce1d-44bf-9e88-e627f6f756f3',
                        task_status='PENDING',
                        task_result=None
                    )
            ),
        ]
    )
    @mock.patch('application.rest_api.housing_units.services.housing_unit_raw_data_ingestion_task')
    @pytest.mark.asyncio
    async def test_apply(
            self,
            mock_housing_unit_raw_data_ingestion_task: MagicMock,
            hbd_dataset_id: Optional[str],
            reset_table: Optional[bool],
            expected_response: Optional[TaskStatus],
    ) -> None:
        mock_housing_unit_raw_data_ingestion_task.delay.return_value = AsyncResult(
            task_name='test',
            id='3f6bf0e4-ce1d-44bf-9e88-e627f6f756f3'
        )
        result = await self.housing_units_data_ingestion_service.apply(
            hbd_dataset_id=hbd_dataset_id,
            reset_table=reset_table,
        )

        assert result == expected_response


class TestFilterHousingUnitsService:

    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.mock_housing_units_repository = AsyncMock()

        self.filter_housing_units_service = FilterHousingUnitsService(
            housing_units_repository=self.mock_housing_units_repository
        )

    @pytest.mark.asyncio
    async def test_apply_raise_error_when_num_max_units_is_smaller_than_num_min_units(self) -> None:
        expected_error: InvalidNumUnitsError = InvalidNumUnitsError(
            "The provided number of maximum units can't be smaller than the number of "
            "minimum units"
        )

        with pytest.raises(InvalidNumUnitsError) as ex:
            await self.filter_housing_units_service.apply(
                num_units_min=2,
                num_units_max=1
            )
        assert ex.value.args == expected_error.args
        assert ex.value.error_type == expected_error.error_type
        assert ex.value.message == expected_error.message

    @pytest.mark.parametrize(
        # Service input.
        'street_name, borough, postcode, construction_type, num_units_min, num_units_max, '
        # Expected Error.
        'expected_response',
        [
            # when_repository_returns_instances
            (
                    'street name test',  # street_name
                    'borough test',  # borough
                    1,  # postcode
                    'construction type test',  # construction_type
                    1,  # num_units_min
                    5,  # num_units_max
                    FilterHousingUnits(
                        housing_units=[
                            HousingUnit(
                                street_name='street name test 1',
                                borough='borough test 1',
                                postcode=1,
                                reporting_construction_type='construction type test 1',
                                total_units=5
                            ),
                            HousingUnit(
                                street_name='street name test 1',
                                borough='borough test 1',
                                postcode=2,
                                reporting_construction_type='construction type test 1',
                                total_units=4
                            )
                        ],
                        total=2
                    )
            ),
            # when_repository_does_not_return_instances
            (
                    'street name test',  # street_name
                    'borough test',  # borough
                    1,  # postcode
                    'construction type test',  # construction_type
                    1,  # num_units_min
                    5,  # num_units_max
                    FilterHousingUnits(
                        housing_units=[],
                        total=0
                    )
            ),
        ]
    )
    @pytest.mark.asyncio
    async def test_apply(
            self,
            street_name: Optional[str],
            borough: Optional[str],
            postcode: Optional[int],
            construction_type: Optional[str],
            num_units_min: Optional[int],
            num_units_max: Optional[int],
            expected_response: Optional[FilterHousingUnits]
    ) -> None:
        self.mock_housing_units_repository.filter.return_value = expected_response.housing_units
        result = await self.filter_housing_units_service.apply(
            street_name=street_name,
            borough=borough,
            postcode=postcode,
            construction_type=construction_type,
            num_units_min=num_units_min,
            num_units_max=num_units_max
        )

        self.mock_housing_units_repository.filter.assert_called_once_with(
            street_name=street_name,
            borough=borough,
            postcode=postcode,
            construction_type=construction_type,
            num_units_min=num_units_min,
            num_units_max=num_units_max
        )

        assert result == expected_response


class TestRetrieveHousingUnitService:

    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.mock_housing_units_repository = AsyncMock()

        self.retrieve_housing_unit_service = RetrieveHousingUnitService(
            housing_units_repository=self.mock_housing_units_repository
        )

    @pytest.mark.asyncio
    async def test_apply_raise_error_when_uuid_not_provided(self) -> None:
        expected_error: InvalidArgumentError = InvalidArgumentError("The uuid is not provided.")

        with pytest.raises(InvalidArgumentError) as ex:
            await self.retrieve_housing_unit_service.apply(
                uuid=None
            )
        assert ex.value.args == expected_error.args
        assert ex.value.error_type == expected_error.error_type
        assert ex.value.message == expected_error.message

    @pytest.mark.asyncio
    async def test_apply(self, stub_housing_units) -> None:
        self.mock_housing_units_repository.get_by_uuid.return_value = stub_housing_units[0]
        result = await self.retrieve_housing_unit_service.apply(uuid=stub_housing_units[0].uuid)

        self.mock_housing_units_repository.get_by_uuid.assert_called_once_with(uuid=stub_housing_units[0].uuid)

        assert result == stub_housing_units[0]


class TestCreateHousingUnitService:

    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.mock_housing_units_repository = AsyncMock()

        self.create_housing_unit_service = CreateHousingUnitService(
            housing_units_repository=self.mock_housing_units_repository
        )

    @pytest.mark.asyncio
    async def test_apply_raise_error_when_body_not_provided(self) -> None:
        expected_error: InvalidArgumentError = InvalidArgumentError("The housing unit body is not provided.")

        with pytest.raises(InvalidArgumentError) as ex:
            await self.create_housing_unit_service.apply(None)

        assert ex.value.args == expected_error.args
        assert ex.value.error_type == expected_error.error_type
        assert ex.value.message == expected_error.message

    @pytest.mark.asyncio
    async def test_apply(self, stub_housing_units, full_housing_unit_request_body) -> None:
        housing_unit_body: HousingUnitPostRequestBody = HousingUnitPostRequestBody(**full_housing_unit_request_body)

        repository_input = HousingUnit(
            project_id=housing_unit_body.project_id,
            project_name=housing_unit_body.project_name,
            project_start_date=housing_unit_body.project_start_date,
            project_completion_date=housing_unit_body.project_completion_date,
            building_id=housing_unit_body.building_id,
            house_number=housing_unit_body.house_number,
            street_name=housing_unit_body.street_name,
            borough=housing_unit_body.borough,
            postcode=housing_unit_body.postcode,
            bbl=housing_unit_body.bbl,
            bin=housing_unit_body.bin,
            community_board=housing_unit_body.community_board,
            council_district=housing_unit_body.council_district,
            census_tract=housing_unit_body.census_tract,
            neighborhood_tabulation_area=housing_unit_body.neighborhood_tabulation_area,
            latitude=housing_unit_body.latitude,
            longitude=housing_unit_body.longitude,
            latitude_internal=housing_unit_body.latitude_internal,
            longitude_internal=housing_unit_body.longitude_internal,
            building_completion_date=housing_unit_body.building_completion_date,
            reporting_construction_type=housing_unit_body.reporting_construction_type,
            extended_affordability_status=housing_unit_body.extended_affordability_status,
            prevailing_wage_status=housing_unit_body.prevailing_wage_status,
            extremely_low_income_units=housing_unit_body.extremely_low_income_units,
            very_low_income_units=housing_unit_body.very_low_income_units,
            low_income_units=housing_unit_body.low_income_units,
            moderate_income_units=housing_unit_body.moderate_income_units,
            middle_income_units=housing_unit_body.middle_income_units,
            other_income_units=housing_unit_body.other_income_units,
            studio_units=housing_unit_body.studio_units,
            one_br_units=housing_unit_body.one_br_units,
            two_br_units=housing_unit_body.two_br_units,
            three_br_units=housing_unit_body.three_br_units,
            four_br_units=housing_unit_body.four_br_units,
            five_br_units=housing_unit_body.five_br_units,
            six_br_units=housing_unit_body.six_br_units,
            unknown_br_units=housing_unit_body.unknown_br_units,
            counted_rental_units=housing_unit_body.counted_rental_units,
            counted_homeownership_units=housing_unit_body.counted_homeownership_units,
            all_counted_units=housing_unit_body.all_counted_units,
            total_units=housing_unit_body.total_units,
        )
        self.mock_housing_units_repository.save.return_value = repository_input

        self.mock_housing_units_repository.get_by_uuid.return_value = stub_housing_units[0]
        result = await self.create_housing_unit_service.apply(housing_unit_body)

        self.mock_housing_units_repository.save.assert_called_once_with(repository_input)

        assert result == repository_input
