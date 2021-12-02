from typing import Dict

from pandas import DataFrame
from sodapy import Socrata

from application.infrastructure.configurations.models import Configuration
from application.infrastructure.error.errors import NoneArgumentError
import pandas as pd


class SocrataClient:

    DTYPES: Dict[str, str] = {
        'project_id': 'object',
        'project_name': 'object',
        'project_start_date': 'datetime64',
        'project_completion_date': 'datetime64',
        'building_id': 'Int64',
        'house_number': 'object',
        'street_name': 'object',
        'borough': 'object',
        'postcode': 'Int64',
        'bbl': 'Int64',
        'bin': 'Int64',
        'community_board': 'object',
        'council_district': 'Int64',
        'census_tract': 'object',
        'neighborhood_tabulation_area': 'object',
        'latitude': 'Int64',
        'longitude': 'Int64',
        'latitude_internal': 'Int64',
        'longitude_internal': 'Int64',
        'building_completion_date': 'datetime64',
        'reporting_construction_type': 'object',
        'extended_affordability_status': 'object',
        'prevailing_wage_status': 'object',
        'extremely_low_income_units': 'Int64',
        'very_low_income_units': 'Int64',
        'low_income_units': 'Int64',
        'moderate_income_units': 'Int64',
        'middle_income_units': 'Int64',
        'other_income_units': 'Int64',
        'studio_units': 'Int64',
        '_1_br_units': 'Int64',
        '_2_br_units': 'Int64',
        '_3_br_units': 'Int64',
        '_4_br_units': 'Int64',
        '_5_br_units': 'Int64',
        '_6_br_units': 'Int64',
        'unknown_br_units': 'Int64',
        'counted_rental_units': 'Int64',
        'counted_homeownership_units': 'Int64',
        'all_counted_units': 'Int64',
        'total_units': 'Int64',
    }
    CHUNK_SIZE = 500

    def __init__(self, hbd_dataset_id: str = 'hg8x-zxpr'):
        if not hbd_dataset_id:
            raise NoneArgumentError("HBD Dataset ID is not provided.")

        self._dataset_id: str = hbd_dataset_id
        self._client = Socrata("data.cityofnewyork.us", None)
        self._client = Socrata(
            "data.cityofnewyork.us",
            app_token=Configuration.get().socrata_app_token
        )

        self._dataset_size = 10000

    def download_housing_units_dataset(self) -> DataFrame:
        """
        Downloads the Housing Units dataset by providing the dataset id from the Socrata api.

        :return: The dataframe containing the downloaded results.
        """
        results = self._client.get(self._dataset_id, limit=self._dataset_size)

        # Convert to pandas DataFrame and change the column types.
        dataframe: DataFrame = pd.DataFrame.from_records(results)
        for col, col_type in self.DTYPES.items():
            if col_type == 'Int64':
                dataframe[col] = pd.to_numeric(dataframe[col])

        return dataframe

    @classmethod
    def housing_unit_dataset_generator(cls, housing_unit_dataset: DataFrame) -> DataFrame:
        """
        Breaks the Housing Unit dataset into chunks and create a generator out of them.

        :return: The yielded chunked dataframe.
        """
        for pos in range(0, len(housing_unit_dataset), cls.CHUNK_SIZE):
            yield housing_unit_dataset.iloc[pos:pos + cls.CHUNK_SIZE]
