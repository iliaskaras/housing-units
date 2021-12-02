from celery.result import AsyncResult

from application.infrastructure.error.errors import NoneArgumentError
from application.rest_api.task_status.schemas import TaskStatus


class GetTaskStatusReportService:

    def apply(self, task_id: str) -> TaskStatus:
        """
        Reports the task id state details.

        :param task_id: The Celery task id.

        :return TaskStatus: The Task status details.

        :raises NoneArgumentError: When task_id is not provided.
        """
        if not task_id:
            raise NoneArgumentError("Task id is required.")

        task_result = AsyncResult(task_id)

        return TaskStatus(
            task_id=task_id,
            task_status=task_result.status,
            task_result=task_result.result
        )
