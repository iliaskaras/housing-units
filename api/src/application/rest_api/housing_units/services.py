from application.infrastructure.error.errors import InvalidArgumentError
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
