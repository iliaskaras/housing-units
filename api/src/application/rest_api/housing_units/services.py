from typing import Optional, List

from application.housing_units.models import HousingUnit
from application.housing_units.repositories import HousingUnitsRepository
from application.infrastructure.error.errors import InvalidArgumentError
from application.rest_api.housing_units.errors import InvalidNumUnitsError
from application.rest_api.housing_units.schemas import FilterHousingUnits, HousingUnitPostRequestBody
from application.rest_api.task_status.schemas import TaskStatus
from application.socrata.tasks import housing_unit_raw_data_ingestion_task
from application.task_status.services import GetTaskStatusReportService


class HousingUnitsDataIngestionService:

    def __init__(
            self,
            get_task_status_report_service: GetTaskStatusReportService,
    ) -> None:
        self._get_task_status_report_service: GetTaskStatusReportService = get_task_status_report_service

    async def apply(self, hbd_dataset_id: str = 'hg8x-zxpr', reset_table: bool = True) -> TaskStatus:
        """
        Data ingestion of the raw Housing Preservation and Development (HBD) data into the into the HousingUnit table.
        The actual operation is executed in a celery task housing_unit_raw_data_ingestion_task.

        :param hbd_dataset_id: The HBD dataset id to download and ingest into HousingUnit table.
        :param reset_table: Flag for resetting the saved table data.

        :return: The celery task status that the data ingestion is executed under.

        :raises InvalidArgumentError: If the HBD dataset id is not provided.
        """
        if not hbd_dataset_id:
            raise InvalidArgumentError("The HBD dataset id is not provided.")

        task = housing_unit_raw_data_ingestion_task.delay(hbd_dataset_id, reset_table)

        return self._get_task_status_report_service.apply(task_id=task.id)


class FilterHousingUnitsService:

    def __init__(
            self,
            housing_units_repository: HousingUnitsRepository,
    ) -> None:
        self._housing_units_repository: HousingUnitsRepository = housing_units_repository

    async def apply(
            self,
            street_name: Optional[str] = None,
            borough: Optional[str] = None,
            postcode: Optional[str] = None,
            construction_type: Optional[str] = None,
            num_units_min: Optional[int] = None,
            num_units_max: Optional[int] = None,
    ) -> FilterHousingUnits:
        """
        Service that filters the HousingUnits based on the provided filtering fields.

        :param street_name: The Housing Unit street name.
        :param borough: The Housing Unit borough.
        :param postcode: The Housing Unit postcode.
        :param construction_type: The Housing Unit construction type.
        :param num_units_min: The Housing Unit num_units_min.
        :param num_units_max: The Housing Unit num_units_max.

        :return: The Housing Units retrieved from the filtering, and a number indicating the total number of results.

        :raises InvalidNumUnitsErrors: When the num_units_max is smaller than num_units_min.
        """
        if num_units_max is not None and num_units_min is not None:
            if num_units_max < num_units_min:
                raise InvalidNumUnitsError(
                    "The provided number of maximum units can't be smaller than the number of minimum units"
                )

        housing_units: List[HousingUnit] = await self._housing_units_repository.filter(
            street_name=street_name,
            borough=borough,
            postcode=postcode,
            construction_type=construction_type,
            num_units_min=num_units_min,
            num_units_max=num_units_max,
        )

        return FilterHousingUnits(
            housing_units=housing_units,
            total=len(housing_units)
        )


class RetrieveHousingUnitService:

    def __init__(
            self,
            housing_units_repository: HousingUnitsRepository,
    ) -> None:
        self._housing_units_repository: HousingUnitsRepository = housing_units_repository

    async def apply(
            self,
            uuid: str = None,
    ) -> HousingUnit:
        """
        Service that retrieves the HousingUnit based on the provided id.

        :param uuid: The Housing Unit uuid.

        :return: The Housing Units retrieved from the provided uuid.

        :raises InvalidArgumentError: When the num_units_max is smaller than num_units_min.
        """
        if not uuid:
            raise InvalidArgumentError("The uuid is not provided.")

        housing_unit: HousingUnit = await self._housing_units_repository.get_by_uuid(uuid=uuid)

        return housing_unit


class HousingUnitFieldsSanityCheckService:

    def apply(
            self,
            housing_unit: HousingUnit = None,
    ) -> None:
        """
        Service that makes a sanity checking to a HousingUnit fields.

        :param housing_unit: The Housing Unit to perform the sanity check.

        :raises InvalidArgumentError: When the housing unit is not provided.
                InvalidNumUnitsError: When there are errors with the sanity check on the unit input fields.
        """
        if not housing_unit:
            raise InvalidArgumentError("The housing unit is not provided.")

        error_messages: List[str] = []

        total_number_of_all_units: int = housing_unit.one_br_units + housing_unit.two_br_units \
                                         + housing_unit.three_br_units + housing_unit.four_br_units \
                                         + housing_unit.five_br_units + housing_unit.six_br_units \
                                         + housing_unit.studio_units + housing_unit.unknown_br_units

        if housing_unit.total_units < housing_unit.counted_rental_units:
            error_messages.append("The new total units can't be greater than the counted rental units.")

        if total_number_of_all_units > housing_unit.total_units:
            error_messages.append("The new total number of units can't be greater than the total units.")

        if total_number_of_all_units != housing_unit.all_counted_units:
            error_messages.append("The new total number of units can't be different than the all counted units.")

        if total_number_of_all_units < housing_unit.counted_homeownership_units:
            error_messages.append(
                "The new total number of units can't be smaller than the counted home ownership units."
            )

        total_number_of_income_units: int = housing_unit.extremely_low_income_units \
                                            + housing_unit.very_low_income_units \
                                            + housing_unit.low_income_units \
                                            + housing_unit.moderate_income_units \
                                            + housing_unit.middle_income_units \
                                            + housing_unit.other_income_units

        if total_number_of_income_units != total_number_of_all_units:
            error_messages.append(
                "The new total number of income units can't be different than the new total number of all units."
            )

        if total_number_of_income_units > housing_unit.total_units:
            error_messages.append("The new total number of income units can't be greater than the total units.")

        if total_number_of_income_units != housing_unit.all_counted_units:
            error_messages.append(
                "The new total number of income units can't be different than the all counted units."
            )

        if total_number_of_all_units < housing_unit.counted_homeownership_units:
            error_messages.append(
                "The new total number of income units can't be smaller than the counted home ownership units."
            )

        if error_messages:
            raise InvalidNumUnitsError(', '.join(error_messages))


class CreateHousingUnitService:

    def __init__(
            self,
            housing_units_repository: HousingUnitsRepository,
            housing_unit_fields_sanity_check_service: HousingUnitFieldsSanityCheckService
    ) -> None:
        self._housing_units_repository: HousingUnitsRepository = housing_units_repository
        self._housing_unit_fields_sanity_check_service: HousingUnitFieldsSanityCheckService = \
            housing_unit_fields_sanity_check_service

    async def apply(
            self,
            housing_unit_body: HousingUnitPostRequestBody = None,
    ) -> HousingUnit:
        """
        Service that creates the HousingUnit based on the provided housing unit body.

        :param housing_unit_body: The Housing Unit fields.

        :return: The Housing Units created from the provided body.

        :raises InvalidArgumentError: When the housing_unit_body is not provided.
        """
        if not housing_unit_body:
            raise InvalidArgumentError("The housing unit body is not provided.")

        housing_unit: HousingUnit = HousingUnit(
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

        self._housing_unit_fields_sanity_check_service.apply(housing_unit=housing_unit)

        housing_unit: HousingUnit = await self._housing_units_repository.save(housing_unit=housing_unit)

        return housing_unit


class UpdateHousingUnitService:

    def __init__(
            self,
            housing_units_repository: HousingUnitsRepository,
            housing_unit_fields_sanity_check_service: HousingUnitFieldsSanityCheckService
    ) -> None:
        self._housing_units_repository: HousingUnitsRepository = housing_units_repository
        self._housing_unit_fields_sanity_check_service: HousingUnitFieldsSanityCheckService = \
            housing_unit_fields_sanity_check_service

    async def apply(
            self,
            uuid: str = None,
            housing_unit_body: HousingUnitPostRequestBody = None,
    ) -> HousingUnit:
        """
        Service that updates the HousingUnit by uuid using the provided housing unit body.

        :param uuid: The Housing Unit uuid.
        :param housing_unit_body: The Housing Unit fields.

        :return: The Housing Units updated from the provided body.

        :raises InvalidArgumentError: When the housing_unit_body is not provided.
                InvalidArgumentError: When the uuid is not provided.
        """
        if not housing_unit_body:
            raise InvalidArgumentError("The housing unit body is not provided.")
        if not uuid:
            raise InvalidArgumentError("The uuid is not provided.")

        housing_unit: HousingUnit = await self._housing_units_repository.get_by_uuid(uuid=uuid)

        housing_unit.project_id = housing_unit_body.project_id
        housing_unit.project_name = housing_unit_body.project_name
        housing_unit.project_start_date = housing_unit_body.project_start_date
        housing_unit.project_completion_date = housing_unit_body.project_completion_date
        housing_unit.building_id = housing_unit_body.building_id
        housing_unit.house_number = housing_unit_body.house_number
        housing_unit.street_name = housing_unit_body.street_name
        housing_unit.borough = housing_unit_body.borough
        housing_unit.postcode = housing_unit_body.postcode
        housing_unit.bbl = housing_unit_body.bbl
        housing_unit.bin = housing_unit_body.bin
        housing_unit.community_board = housing_unit_body.community_board
        housing_unit.council_district = housing_unit_body.council_district
        housing_unit.census_tract = housing_unit_body.census_tract
        housing_unit.neighborhood_tabulation_area = housing_unit_body.neighborhood_tabulation_area
        housing_unit.latitude = housing_unit_body.latitude
        housing_unit.longitude = housing_unit_body.longitude
        housing_unit.latitude_internal = housing_unit_body.latitude_internal
        housing_unit.longitude_internal = housing_unit_body.longitude_internal
        housing_unit.building_completion_date = housing_unit_body.building_completion_date
        housing_unit.reporting_construction_type = housing_unit_body.reporting_construction_type
        housing_unit.extended_affordability_status = housing_unit_body.extended_affordability_status
        housing_unit.prevailing_wage_status = housing_unit_body.prevailing_wage_status
        housing_unit.extremely_low_income_units = housing_unit_body.extremely_low_income_units
        housing_unit.very_low_income_units = housing_unit_body.very_low_income_units
        housing_unit.low_income_units = housing_unit_body.low_income_units
        housing_unit.moderate_income_units = housing_unit_body.moderate_income_units
        housing_unit.middle_income_units = housing_unit_body.middle_income_units
        housing_unit.other_income_units = housing_unit_body.other_income_units
        housing_unit.studio_units = housing_unit_body.studio_units
        housing_unit.one_br_units = housing_unit_body.one_br_units
        housing_unit.two_br_units = housing_unit_body.two_br_units
        housing_unit.three_br_units = housing_unit_body.three_br_units
        housing_unit.four_br_units = housing_unit_body.four_br_units
        housing_unit.five_br_units = housing_unit_body.five_br_units
        housing_unit.six_br_units = housing_unit_body.six_br_units
        housing_unit.unknown_br_units = housing_unit_body.unknown_br_units
        housing_unit.counted_rental_units = housing_unit_body.counted_rental_units
        housing_unit.counted_homeownership_units = housing_unit_body.counted_homeownership_units
        housing_unit.all_counted_units = housing_unit_body.all_counted_units
        housing_unit.total_units = housing_unit_body.total_units

        self._housing_unit_fields_sanity_check_service.apply(housing_unit=housing_unit)

        return await self._housing_units_repository.save(housing_unit=housing_unit)
