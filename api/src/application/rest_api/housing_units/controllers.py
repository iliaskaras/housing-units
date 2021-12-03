from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from application.authentication.utils import BearerJWTAuthorizationService
from application.housing_units.container import HousingUnitsContainer
from application.rest_api.housing_units.schemas import DataIngestionPostRequestBody, \
    FilterHousingUnitsGetRequestParameters, FilterHousingUnits, FullHousingUnitResponse, HousingUnitPostRequestBody
from application.rest_api.housing_units.services import HousingUnitsDataIngestionService, FilterHousingUnitsService, \
    RetrieveHousingUnitService, CreateHousingUnitService
from application.rest_api.task_status.schemas import TaskStatus

from application.users.enums import Group

router = APIRouter()


@router.post(
    "/housing-units/data-ingestion",
    dependencies=[Depends(BearerJWTAuthorizationService(permission_groups=[Group.admin]))],
    response_description="Housing Units data ingestion endpoint.",
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
    :param housing_units_data_ingestion_service:  The service responsible for the HousingUnit dataset download and
        ingestion to the HousingUnit table.

    :return: The TaskStatus that executes the data ingestion process.
    """
    return await housing_units_data_ingestion_service.apply(
        hbd_dataset_id=data_ingestion_post_request_body.dataset_id,
        reset_table=data_ingestion_post_request_body.reset_table
    )


@router.get(
    "/housing-units",
    dependencies=[Depends(BearerJWTAuthorizationService(permission_groups=[Group.customer, Group.admin]))],
    response_description="Get Housing Units endpoint.",
    response_model=FilterHousingUnits,
    status_code=200
)
@inject
async def get_housing_units(
        filter_housing_units_get_request_parameters: FilterHousingUnitsGetRequestParameters = Depends(
            FilterHousingUnitsGetRequestParameters
        ),
        filter_housing_units_service: FilterHousingUnitsService = Depends(
            Provide[HousingUnitsContainer.filter_housing_units_service]
        )
):
    """
    Controller for filtering the housing units.

    :param filter_housing_units_get_request_parameters: The data ingestion POST request body.
    :param filter_housing_units_service:  The service responsible for filtering and returning the HousingUnits
     from the HousingUnit table.

    :return: The filtered HousingUnits.
    """
    return await filter_housing_units_service.apply(
        street_name=filter_housing_units_get_request_parameters.street_name,
        borough=filter_housing_units_get_request_parameters.borough,
        postcode=filter_housing_units_get_request_parameters.postcode,
        construction_type=filter_housing_units_get_request_parameters.construction_type,
        num_units_min=filter_housing_units_get_request_parameters.num_units_min,
        num_units_max=filter_housing_units_get_request_parameters.num_units_max
    )


@router.get(
    "/housing-units/{housing_unit_id}",
    dependencies=[Depends(BearerJWTAuthorizationService(permission_groups=[Group.customer, Group.admin]))],
    response_description="Get Housing Unit endpoint.",
    response_model=FullHousingUnitResponse,
    status_code=200
)
@inject
async def get_housing_unit(
        housing_unit_id: str,
        retrieve_housing_unit_service: RetrieveHousingUnitService = Depends(
            Provide[HousingUnitsContainer.retrieve_housing_unit_service]
        )
):
    """
    Controller for returning the housing unit by id.

    :param housing_unit_id: The provided housing unit id.
    :param retrieve_housing_unit_service:  The service responsible for retrieving and returning the HousingUnit
     by uuid from the HousingUnit table.

    :return: The filtered HousingUnits.
    """
    return await retrieve_housing_unit_service.apply(uuid=housing_unit_id)


@router.post(
    "/housing-units/",
    dependencies=[Depends(BearerJWTAuthorizationService(permission_groups=[Group.customer, Group.admin]))],
    response_description="Post Housing Unit endpoint.",
    response_model=FullHousingUnitResponse,
    status_code=200
)
@inject
async def post_housing_unit(
        housing_unit_post_request_body: HousingUnitPostRequestBody,
        create_housing_unit_service: CreateHousingUnitService = Depends(
            Provide[HousingUnitsContainer.create_housing_unit_service]
        )
):
    """
    Controller for creating a HousingUnit entry.

    :param housing_unit_post_request_body: The housing unit body.
    :param create_housing_unit_service:  The service responsible for creating the HousingUnit.

    :return: The created HousingUnits.
    """
    return await create_housing_unit_service.apply(housing_unit_body=housing_unit_post_request_body)
