from typing import Optional, List

from application.housing_units.models import HousingUnit
from application.housing_units.repositories import HousingUnitsRepository
from application.infrastructure.error.errors import InvalidArgumentError
from application.rest_api.housing_units.errors import InvalidNumUnitsError
from application.rest_api.housing_units.schemas import FilterHousingUnits
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

        :raises InvalidNumUnitsErrors: When the num_units_max is smaller than num_units_min.
        """
        if not uuid:
            raise InvalidArgumentError("The uuid is not provided.")

        housing_unit: HousingUnit = await self._housing_units_repository.get_by_uuid(uuid=uuid)

        return housing_unit
