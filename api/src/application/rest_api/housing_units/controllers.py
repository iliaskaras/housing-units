from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from application.authentication.utils import BearerJWTAuthorizationService
from application.housing_units.container import HousingUnitsContainer
from application.rest_api.housing_units.schemas import DataIngestionPostRequestBody
from application.rest_api.housing_units.services import HousingUnitsDataIngestionService
from application.rest_api.task_status.schemas import TaskStatus

from application.users.enums import Group

router = APIRouter()


@router.post(
    "/housing-units/data-ingestion",
    dependencies=[Depends(BearerJWTAuthorizationService(permission_groups=[Group.admin]))],
    response_description="HBD Buildings data ingestion endpoint.",
    response_model=TaskStatus,
    status_code=202
)
@inject
async def housing_units_data_ingestion(
        data_ingestion_post_request_body: DataIngestionPostRequestBody,
        housing_units_data_ingestion_service: HousingUnitsDataIngestionService = Depends(
            Provide[HousingUnitsContainer.housing_units_data_ingestion_service]
        )
):
    """
    Controller for ingesting the housing units data to the database.

    :param data_ingestion_post_request_body: The data ingestion POST request body.
    :param housing_units_data_ingestion_service:  The service responsible for the HBDBuilding dataset download and
        ingestion to the HBDBuilding table.

    :return: The TaskStatus that executes the data ingestion process.
    """
    return await housing_units_data_ingestion_service.apply(
        dataset_id=data_ingestion_post_request_body.dataset_id,
        reset_table=data_ingestion_post_request_body.reset_table
    )
