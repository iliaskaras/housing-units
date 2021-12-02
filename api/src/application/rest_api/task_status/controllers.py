from fastapi import APIRouter, Depends

from application.authentication.utils import BearerJWTAuthorizationService
from application.rest_api.task_status.schemas import TaskStatus
from application.task_status.services import GetTaskStatusReportService
from application.users.enums import Group

router = APIRouter()


@router.get(
    "/task-status/{task_id}",
    dependencies=[Depends(BearerJWTAuthorizationService(permission_groups=[Group.admin]))],
    response_description="Task status reporting endpoint.",
    response_model=TaskStatus,
    status_code=200
)
def get_task_status_details(task_id: str) -> TaskStatus:
    """
    Entrypoint for celery task status monitoring.

    :param task_id: The celery task id.

    :return The task status report.
    """
    return GetTaskStatusReportService().apply(task_id=task_id)
