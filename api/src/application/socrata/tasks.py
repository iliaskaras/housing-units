from typing import List

from pandas import DataFrame

from application.celery_worker import celery
from application.housing_units.models import HBDBuilding
from application.housing_units.repositories import HBDBuildingRepository

from application.infrastructure.database.database import DatabaseEngineWrapper
from application.socrata.client import SocrataClient
from application.socrata.errors import SocrataDatasetDownloadError


@celery.task(name="housing_units_data_ingestion")
def hbd_raw_data_ingestion_task(dataset_id: str = 'hg8x-zxpr', reset_table: bool = True) -> str:
    """
    Celery Task for executing the HBD Building table data ingestion process.

    :param dataset_id: The HBD Dataset id, that we want to download using Socrata API.
    :param reset_table: Flag for resetting the saved table data.

    :return: A string representing the number of rows inserted.

    :raises SocrataDatasetDownloadError: When there is an error raised on dataset download from SocrataClient.
    """
    hbd_building_repository: HBDBuildingRepository = HBDBuildingRepository(db_engine=DatabaseEngineWrapper())
    socrata_client: SocrataClient = SocrataClient(dataset_id=dataset_id)

    try:
        results_df: DataFrame = socrata_client.download_hbd_building_dataset()
    except Exception as ex:
        raise SocrataDatasetDownloadError(
            "Failed to download the dataset id {0} "
            "from Socrata api with the following error: {1}".format(dataset_id, ex)
        )

    if reset_table:
        hbd_building_repository.truncate_table()

    hbd_buildings: List[HBDBuilding] = []
    for _chunk in socrata_client.hbd_building_dataset_generator(results_df):
        for index, row in _chunk.T.to_dict().items():
            try:
                hbd_buildings.append(HBDBuilding.from_dict(row))
            except Exception as ex:
                print(ex)

        hbd_building_repository.bulk_save(hbd_buildings)

    return 'Number of rows inserted: {0}.'.format(len(hbd_buildings))
