from dependency_injector import containers, providers
from dependency_injector.providers import Singleton

from application.housing_units.repositories import HousingUnitsRepository
from application.infrastructure.database.database import DatabaseEngineWrapper
from application.rest_api.housing_units.services import HousingUnitsDataIngestionService, FilterHousingUnitsService, \
    RetrieveHousingUnitService, CreateHousingUnitService, UpdateHousingUnitService, HousingUnitFieldsSanityCheckService, \
    DeleteHousingUnitService
from application.task_status.services import GetTaskStatusReportService


class HousingUnitsContainer(containers.DeclarativeContainer):
    """
    User inversion of control Housing Units.
    """

    wiring_config = containers.WiringConfiguration(
        modules=[
            "..rest_api.housing_units.controllers",
        ]
    )

    housing_units_repository: Singleton = providers.Singleton(
        HousingUnitsRepository,
        db_engine=DatabaseEngineWrapper
    )

    housing_units_data_ingestion_service: Singleton = providers.Singleton(
        HousingUnitsDataIngestionService,
        get_task_status_report_service=GetTaskStatusReportService()
    )

    filter_housing_units_service: Singleton = providers.Singleton(
        FilterHousingUnitsService,
        housing_units_repository=housing_units_repository,
    )

    retrieve_housing_unit_service: Singleton = providers.Singleton(
        RetrieveHousingUnitService,
        housing_units_repository=housing_units_repository,
    )

    create_housing_unit_service: Singleton = providers.Singleton(
        CreateHousingUnitService,
        housing_units_repository=housing_units_repository,
        housing_unit_fields_sanity_check_service=HousingUnitFieldsSanityCheckService()
    )

    update_housing_unit_service: Singleton = providers.Singleton(
        UpdateHousingUnitService,
        housing_units_repository=housing_units_repository,
        housing_unit_fields_sanity_check_service=HousingUnitFieldsSanityCheckService()
    )

    delete_housing_unit_service: Singleton = providers.Singleton(
        DeleteHousingUnitService,
        housing_units_repository=housing_units_repository
    )
