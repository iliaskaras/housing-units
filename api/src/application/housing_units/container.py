from dependency_injector import containers, providers
from dependency_injector.providers import Singleton

from application.housing_units.repositories import HousingUnitsRepository
from application.infrastructure.database.database import DatabaseEngineWrapper
from application.rest_api.housing_units.services import HousingUnitsDataIngestionService
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
