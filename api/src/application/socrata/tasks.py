from typing import List

from pandas import DataFrame

from application.celery_worker import celery
from application.housing_units.models import HousingUnit
from application.housing_units.repositories import HousingUnitsRepository

from application.infrastructure.database.database import DatabaseEngineWrapper
from application.socrata.client import SocrataClient
from application.socrata.errors import SocrataDatasetDownloadError


@celery.task(name="housing_units_data_ingestion")
def housing_unit_raw_data_ingestion_task(hbd_dataset_id: str = 'hg8x-zxpr', reset_table: bool = True) -> str:
    """
    Celery Task for executing the Housing Unit table data ingestion process.

    :param hbd_dataset_id: The HBD Dataset id, that we want to download using Socrata API.
    :param reset_table: Flag for resetting the saved table data.

    :return: A string representing the number of rows inserted.

    :raises SocrataDatasetDownloadError: When there is an error raised on dataset download from SocrataClient.
    """
    housing_units_repository: HousingUnitsRepository = HousingUnitsRepository(db_engine=DatabaseEngineWrapper())
    socrata_client: SocrataClient = SocrataClient(hbd_dataset_id=hbd_dataset_id)

    try:
        results_df: DataFrame = socrata_client.download_housing_units_dataset()
    except Exception as ex:
        raise SocrataDatasetDownloadError(
            "Failed to download the dataset id {0} "
            "from Socrata api with the following error: {1}".format(hbd_dataset_id, ex)
        )

    if reset_table:
        housing_units_repository.truncate_table()

    housing_units: List[HousingUnit] = []
    for _chunk in socrata_client.housing_unit_dataset_generator(results_df):
        for index, row in _chunk.T.to_dict().items():
            try:
                housing_units.append(HousingUnit.from_dict(row))
            except Exception as ex:
                print(ex)

        housing_units_repository.bulk_save(housing_units)

    return 'Number of HousingUnits inserted: {0}.'.format(len(housing_units))
