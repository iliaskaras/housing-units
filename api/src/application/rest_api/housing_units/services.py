from application.infrastructure.error.errors import InvalidArgumentError
from application.rest_api.task_status.schemas import TaskStatus
from application.socrata.tasks import hbd_raw_data_ingestion_task
from application.task_status.services import GetTaskStatusReportService


class HousingUnitsDataIngestionService:

    def __init__(
            self,
            get_task_status_report_service: GetTaskStatusReportService,
    ) -> None:
        self._get_task_status_report_service: GetTaskStatusReportService = get_task_status_report_service

    async def apply(self, dataset_id: str = 'hg8x-zxpr', reset_table: bool = True) -> TaskStatus:
        """
        Data ingestion of the raw Housing Preservation and Development (HBD) data into the into the HBDBuilding table.
        The actual operation is executed in a celery task HBDDataIngestionTask.

        :param dataset_id: The dataset id to download and ingest into HBDBuilding table.
        :param reset_table: Flag for resetting the saved table data.

        :return: The celery task status that the data ingestion is executed under.

        :raises InvalidArgumentError: If the dataset id is not provided.
        """
        if not dataset_id:
            raise InvalidArgumentError("Dataset id is not provided.")

        task = hbd_raw_data_ingestion_task.delay(dataset_id, reset_table)

        return self._get_task_status_report_service.apply(task_id=task.id)
