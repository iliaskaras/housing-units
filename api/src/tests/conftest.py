import os

import uuid
from datetime import datetime

from application.authentication.models import JwtBody
from application.authentication.services import GetJWTService
from application.authentication.validators import JwtValidator
from application.infrastructure.configurations.enums import APIEnvironment
from application.infrastructure.configurations.models import API_ENVIRONMENT
from typing import List, Dict

import pytest
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database, drop_database

from application.housing_units.models import HousingUnit
from application.infrastructure.configurations.models import Configuration
from application.infrastructure.database.database import DatabaseEngineWrapper
from application.infrastructure.database.models import HousingUnitsDBBaseModel
from application.rest_api.housing_units.schemas import HousingUnitPostRequestBody
from application.users.enums import Group
from application.users.models import User

os.environ['POSTGRESQL_CONNECTION_URI'] = "postgresql+psycopg2://housing_units_api:123456@" \
                                          "0.0.0.0:5432/housing_units_api_tests"
os.environ['ASYNC_POSTGRESQL_CONNECTION_URI'] = "postgresql+asyncpg://housing_units_api:123456@" \
                                                "127.0.0.1:5432/housing_units_api_tests"
os.environ['CELERY_BROKER_URL'] = "redis://127.0.0.1:6379/0"
os.environ['CELERY_RESULT_BACKEND'] = "redis://127.0.0.1:6379/0"
os.environ['SECRET'] = "32c9c8fd6b25bd81cbe5d64afd835f62cf2ffdd11f9ab321"
os.environ['ALGORITHM'] = "HS256"
os.environ['SOCRATA_APP_TOKEN'] = "bMQxufH6NyYPXWyCwtjYVx1OH"
os.environ[API_ENVIRONMENT] = APIEnvironment.test.value


@pytest.fixture(scope='session')
def configuration() -> None:
    Configuration.initialize()


@pytest.fixture(scope='function', autouse=True)
def db_manager(configuration: None) -> None:
    """
    Creates the Database for the regression and functional tests.
    """

    engine: Engine = create_engine(Configuration.get().postgresql_connection_uri, echo=True)
    if not database_exists(engine.url):
        create_database(engine.url)
    HousingUnitsDBBaseModel.metadata.create_all(engine)

    yield

    drop_database(engine.url)
    engine.dispose()


@pytest.fixture
def stub_users() -> List[User]:
    users: List[User] = [
        User(
            email='admin_user@admin.com',
            password='123456',
            user_group=Group.admin.value,
            is_active=True
        ),
        User(
            email='customer_user@customer.com',
            password='123456',
            user_group=Group.customer.value,
            is_active=True
        ),
    ]

    return users


@pytest.fixture
def stub_housing_units() -> List[HousingUnit]:
    timestamp = 1545730073
    dt_object = datetime.fromtimestamp(timestamp)

    housing_units: List[HousingUnit] = [
        HousingUnit(
            uuid=str(uuid.uuid4()),
            project_id='project id 1',
            street_name='street name test 1',
            borough='Queens',
            postcode=1,
            reporting_construction_type='construction type test 1',
            project_name='project name 1',
            project_start_date=dt_object,
            community_board='community board 1',
            extended_affordability_status='extended affordability status 1',
            prevailing_wage_status='prevailing wage status 1',
            extremely_low_income_units=0,
            very_low_income_units=0,
            low_income_units=0,
            moderate_income_units=0,
            middle_income_units=2,
            other_income_units=0,
            studio_units=0,
            one_br_units=1,
            two_br_units=0,
            three_br_units=1,
            four_br_units=0,
            five_br_units=0,
            six_br_units=0,
            unknown_br_units=0,
            counted_rental_units=1,
            counted_homeownership_units=1,
            all_counted_units=2,
            total_units=2,
        ),
        HousingUnit(
            uuid=str(uuid.uuid4()),
            project_id='project id 2',
            street_name='street name test 2',
            borough='Brooklyn',
            postcode=2,
            reporting_construction_type='construction type test 2',
            project_name='project name 2',
            project_start_date=dt_object,
            community_board='community board 2',
            extended_affordability_status='extended affordability status 2',
            prevailing_wage_status='prevailing wage status 2',
            extremely_low_income_units=0,
            very_low_income_units=0,
            low_income_units=4,
            moderate_income_units=0,
            middle_income_units=0,
            other_income_units=0,
            studio_units=0,
            one_br_units=0,
            two_br_units=0,
            three_br_units=0,
            four_br_units=0,
            five_br_units=0,
            six_br_units=0,
            unknown_br_units=4,
            counted_rental_units=0,
            counted_homeownership_units=4,
            all_counted_units=4,
            total_units=4,
        ),
        HousingUnit(
            uuid=str(uuid.uuid4()),
            project_id='project id 3',
            street_name='street name test 3',
            borough='Staten Island',
            postcode=3,
            reporting_construction_type='construction type test 3',
            project_name='project name 3',
            project_start_date=dt_object,
            community_board='community board 3',
            extended_affordability_status='extended affordability status 3',
            prevailing_wage_status='prevailing wage status 3',
            extremely_low_income_units=0,
            very_low_income_units=0,
            low_income_units=0,
            moderate_income_units=0,
            middle_income_units=2,
            other_income_units=0,
            studio_units=0,
            one_br_units=0,
            two_br_units=2,
            three_br_units=0,
            four_br_units=0,
            five_br_units=0,
            six_br_units=0,
            unknown_br_units=0,
            counted_rental_units=2,
            counted_homeownership_units=0,
            all_counted_units=2,
            total_units=6,
        ),
        HousingUnit(
            uuid=str(uuid.uuid4()),
            project_id='project id 4',
            street_name='street name test 4',
            borough='Manhattan',
            postcode=4,
            reporting_construction_type='construction type test 4',
            project_name='project name 4',
            project_start_date=dt_object,
            community_board='community board 4',
            extended_affordability_status='extended affordability status 4',
            prevailing_wage_status='prevailing wage status 4',
            extremely_low_income_units=0,
            very_low_income_units=0,
            low_income_units=0,
            moderate_income_units=2,
            middle_income_units=6,
            other_income_units=0,
            studio_units=0,
            one_br_units=2,
            two_br_units=6,
            three_br_units=0,
            four_br_units=0,
            five_br_units=0,
            six_br_units=0,
            unknown_br_units=0,
            counted_rental_units=0,
            counted_homeownership_units=8,
            all_counted_units=8,
            total_units=8,
        ),
        HousingUnit(
            uuid=str(uuid.uuid4()),
            project_id='project id 5',
            street_name='street name test 5',
            borough='Bronx',
            postcode=5,
            reporting_construction_type='construction type test 5',
            project_name='project name 5',
            project_start_date=dt_object,
            community_board='community board 5',
            extended_affordability_status='extended affordability status 5',
            prevailing_wage_status='prevailing wage status 5',
            extremely_low_income_units=0,
            very_low_income_units=0,
            low_income_units=0,
            moderate_income_units=10,
            middle_income_units=0,
            other_income_units=0,
            studio_units=0,
            one_br_units=3,
            two_br_units=7,
            three_br_units=0,
            four_br_units=0,
            five_br_units=0,
            six_br_units=0,
            unknown_br_units=0,
            counted_rental_units=0,
            counted_homeownership_units=10,
            all_counted_units=10,
            total_units=10,
        ),
        HousingUnit(
            uuid=str(uuid.uuid4()),
            project_id='project id 6',
            street_name='street name test 1',
            borough='Queens',
            postcode=1,
            reporting_construction_type='construction type test 1',
            project_name='project name 6',
            project_start_date=dt_object,
            community_board='community board 6',
            extended_affordability_status='extended affordability status 6',
            prevailing_wage_status='prevailing wage status 6',
            extremely_low_income_units=5,
            very_low_income_units=6,
            low_income_units=1,
            moderate_income_units=0,
            middle_income_units=0,
            other_income_units=0,
            studio_units=0,
            one_br_units=12,
            two_br_units=0,
            three_br_units=0,
            four_br_units=0,
            five_br_units=0,
            six_br_units=0,
            unknown_br_units=0,
            counted_rental_units=12,
            counted_homeownership_units=0,
            all_counted_units=12,
            total_units=12,
        ),
        HousingUnit(
            uuid=str(uuid.uuid4()),
            project_id='project id 7',
            street_name='street name test 2',
            borough='Brooklyn',
            postcode=2,
            reporting_construction_type='construction type test 2',
            project_name='project name 7',
            project_start_date=dt_object,
            community_board='community board 7',
            extended_affordability_status='extended affordability status 7',
            prevailing_wage_status='prevailing wage status 7',
            extremely_low_income_units=0,
            very_low_income_units=0,
            low_income_units=0,
            moderate_income_units=14,
            middle_income_units=0,
            other_income_units=0,
            studio_units=4,
            one_br_units=0,
            two_br_units=6,
            three_br_units=4,
            four_br_units=0,
            five_br_units=0,
            six_br_units=0,
            unknown_br_units=0,
            counted_rental_units=0,
            counted_homeownership_units=14,
            all_counted_units=14,
            total_units=14,
        ),
        HousingUnit(
            uuid=str(uuid.uuid4()),
            project_id='project id 8',
            street_name='street name test 3',
            borough='Staten Island',
            postcode=3,
            reporting_construction_type='construction type test 3',
            project_name='project name 8',
            project_start_date=dt_object,
            community_board='community board 8',
            extended_affordability_status='extended affordability status 8',
            prevailing_wage_status='prevailing wage status 8',
            extremely_low_income_units=2,
            very_low_income_units=9,
            low_income_units=4,
            moderate_income_units=0,
            middle_income_units=0,
            other_income_units=1,
            studio_units=1,
            one_br_units=6,
            two_br_units=9,
            three_br_units=0,
            four_br_units=0,
            five_br_units=0,
            six_br_units=0,
            unknown_br_units=0,
            counted_rental_units=16,
            counted_homeownership_units=0,
            all_counted_units=16,
            total_units=16,
        ),
        HousingUnit(
            uuid=str(uuid.uuid4()),
            project_id='project id 9',
            street_name='street name test 4',
            borough='Manhattan',
            postcode=4,
            reporting_construction_type='construction type test 4',
            project_name='project name 9',
            project_start_date=dt_object,
            community_board='community board 9',
            extended_affordability_status='extended affordability status 9',
            prevailing_wage_status='prevailing wage status 9',
            extremely_low_income_units=0,
            very_low_income_units=14,
            low_income_units=2,
            moderate_income_units=2,
            middle_income_units=0,
            other_income_units=0,
            studio_units=2,
            one_br_units=10,
            two_br_units=0,
            three_br_units=6,
            four_br_units=0,
            five_br_units=0,
            six_br_units=0,
            unknown_br_units=0,
            counted_rental_units=18,
            counted_homeownership_units=0,
            all_counted_units=18,
            total_units=18,
        ),
        HousingUnit(
            uuid=str(uuid.uuid4()),
            project_id='project id 10',
            street_name='street name test 5',
            borough='Bronx',
            postcode=5,
            reporting_construction_type='construction type test 5',
            project_name='project name 10',
            project_start_date=dt_object,
            community_board='community board 10',
            extended_affordability_status='extended affordability status 10',
            prevailing_wage_status='prevailing wage status 10',
            extremely_low_income_units=3,
            very_low_income_units=17,
            low_income_units=0,
            moderate_income_units=0,
            middle_income_units=0,
            other_income_units=0,
            studio_units=1,
            one_br_units=9,
            two_br_units=10,
            three_br_units=0,
            four_br_units=0,
            five_br_units=0,
            six_br_units=0,
            unknown_br_units=0,
            counted_rental_units=20,
            counted_homeownership_units=0,
            all_counted_units=20,
            total_units=20,
        ),
        HousingUnit(
            uuid=str(uuid.uuid4()),
            project_id='project id 11',
            street_name='street name test 1',
            borough='Queens',
            postcode=1,
            reporting_construction_type='construction type test 1',
            project_name='project name 11',
            project_start_date=dt_object,
            community_board='community board 11',
            extended_affordability_status='extended affordability status 11',
            prevailing_wage_status='prevailing wage status 11',
            extremely_low_income_units=2,
            very_low_income_units=9,
            low_income_units=4,
            moderate_income_units=13,
            middle_income_units=0,
            other_income_units=1,
            studio_units=1,
            one_br_units=6,
            two_br_units=9,
            three_br_units=0,
            four_br_units=0,
            five_br_units=0,
            six_br_units=0,
            unknown_br_units=0,
            counted_rental_units=16,
            counted_homeownership_units=0,
            all_counted_units=16,
            total_units=16,
        ),
        HousingUnit(
            uuid=str(uuid.uuid4()),
            project_id='project id 12',
            street_name='street name test 1',
            borough='Queens',
            postcode=1,
            reporting_construction_type='construction type test 1',
            project_name='project name 12',
            project_start_date=dt_object,
            community_board='community board 12',
            extended_affordability_status='extended affordability status 12',
            prevailing_wage_status='prevailing wage status 12',
            extremely_low_income_units=10,
            very_low_income_units=6,
            low_income_units=9,
            moderate_income_units=0,
            middle_income_units=0,
            other_income_units=0,
            studio_units=13,
            one_br_units=7,
            two_br_units=5,
            three_br_units=0,
            four_br_units=0,
            five_br_units=0,
            six_br_units=0,
            unknown_br_units=0,
            counted_rental_units=25,
            counted_homeownership_units=0,
            all_counted_units=25,
            total_units=25,
        ),
        HousingUnit(
            uuid=str(uuid.uuid4()),
            project_id='project id 12',
            street_name='street name test 1',
            borough='Queens',
            postcode=1,
            reporting_construction_type='construction type test 1',
            project_name='project name 13',
            project_start_date=dt_object,
            community_board='community board 13',
            extended_affordability_status='extended affordability status 13',
            prevailing_wage_status='prevailing wage status 13',
            extremely_low_income_units=10,
            very_low_income_units=6,
            low_income_units=9,
            moderate_income_units=0,
            middle_income_units=0,
            other_income_units=0,
            studio_units=13,
            one_br_units=7,
            two_br_units=5,
            three_br_units=0,
            four_br_units=0,
            five_br_units=0,
            six_br_units=0,
            unknown_br_units=0,
            counted_rental_units=25,
            counted_homeownership_units=0,
            all_counted_units=25,
            total_units=25,
        ),
    ]

    return housing_units


@pytest.fixture
def populate_housing_units(db_manager, stub_housing_units) -> None:
    """
    Populates the HousingUnits table.

    :param db_manager: Fixture that responsible for creating and deleting the test database.
    :param stub_housing_units: The housing units to ingest into the table.
    """

    engine = create_engine(
        url=Configuration.get().postgresql_connection_uri,
        echo=True
    )

    Session = sessionmaker(engine, expire_on_commit=False)
    with Session() as session:
        with session.begin():
            session.add_all(stub_housing_units)

    yield

    DatabaseEngineWrapper.reset()


@pytest.fixture
def populate_users(db_manager, stub_users) -> None:
    """
    Populates the Users table.

    :param db_manager: Fixture that responsible for creating and deleting the test database.
    :param stub_users: The users to ingest into the table.
    """

    engine = create_engine(
        url=Configuration.get().postgresql_connection_uri,
        echo=True
    )

    Session = sessionmaker(engine, expire_on_commit=False)
    with Session() as session:
        with session.begin():
            session.add_all(stub_users)

    yield

    DatabaseEngineWrapper.reset()


@pytest.fixture
def admin_jwt_token() -> str:
    """
    Returns a JWT Token for admins.
    """
    access_token = GetJWTService(
        jwt_validator=JwtValidator(),
        config=Configuration.get()
    ).apply(
        jwt_body=JwtBody(
            user_id='admin_user@admin.com',
            group=Group.admin.value
        )
    )

    return access_token


@pytest.fixture
def customer_jwt_token() -> str:
    """
    Returns a JWT Token for admins.
    """
    access_token = GetJWTService(
        jwt_validator=JwtValidator(),
        config=Configuration.get()
    ).apply(
        jwt_body=JwtBody(
            user_id='customer_user@customer.com',
            group=Group.admin.value
        )
    )

    return access_token


@pytest.fixture
def full_housing_unit_request_body() -> Dict[str, str]:
    """
    Returns a dictionary with all the housing unit fields used in post and put requests.
    """

    return {
        "project_id": "44223",
        "street_name": "RALPH AVENUE",
        "borough": "Brooklyn",
        "postcode": None,
        "reporting_construction_type": "New Construction",
        "total_units": 10,
        "project_name": "ROCHESTER SUYDAM PHASE 1",
        "project_start_date": "2021-06-30T00:00:00",
        "project_completion_date": None,
        "building_id": 977564,
        "house_number": "329/331",
        "bbl": None,
        "bin": None,
        "community_board": "BK-03",
        "council_district": 977564,
        "census_tract": None,
        "neighborhood_tabulation_area": None,
        "latitude": None,
        "longitude": None,
        "latitude_internal": None,
        "longitude_internal": None,
        "building_completion_date": None,
        "extended_affordability_status": "No",
        "prevailing_wage_status": "Non Prevailing Wage",
        "extremely_low_income_units": 0,
        "very_low_income_units": 0,
        "low_income_units": 0,
        "moderate_income_units": 10,
        "middle_income_units": 0,
        "other_income_units": 0,
        "studio_units": 0,
        "one_br_units": 3,
        "two_br_units": 7,
        "three_br_units": 0,
        "four_br_units": 0,
        "five_br_units": 0,
        "six_br_units": 0,
        "unknown_br_units": 0,
        "counted_rental_units": 0,
        "counted_homeownership_units": 10,
        "all_counted_units": 10
    }


@pytest.fixture
def housing_unit_repository_input(full_housing_unit_request_body) -> HousingUnit:
    housing_unit_body: HousingUnitPostRequestBody = HousingUnitPostRequestBody(**full_housing_unit_request_body)

    return HousingUnit(
        project_id=housing_unit_body.project_id,
        project_name=housing_unit_body.project_name,
        project_start_date=housing_unit_body.project_start_date,
        project_completion_date=housing_unit_body.project_completion_date,
        building_id=housing_unit_body.building_id,
        house_number=housing_unit_body.house_number,
        street_name=housing_unit_body.street_name,
        borough=housing_unit_body.borough,
        postcode=housing_unit_body.postcode,
        bbl=housing_unit_body.bbl,
        bin=housing_unit_body.bin,
        community_board=housing_unit_body.community_board,
        council_district=housing_unit_body.council_district,
        census_tract=housing_unit_body.census_tract,
        neighborhood_tabulation_area=housing_unit_body.neighborhood_tabulation_area,
        latitude=housing_unit_body.latitude,
        longitude=housing_unit_body.longitude,
        latitude_internal=housing_unit_body.latitude_internal,
        longitude_internal=housing_unit_body.longitude_internal,
        building_completion_date=housing_unit_body.building_completion_date,
        reporting_construction_type=housing_unit_body.reporting_construction_type,
        extended_affordability_status=housing_unit_body.extended_affordability_status,
        prevailing_wage_status=housing_unit_body.prevailing_wage_status,
        extremely_low_income_units=housing_unit_body.extremely_low_income_units,
        very_low_income_units=housing_unit_body.very_low_income_units,
        low_income_units=housing_unit_body.low_income_units,
        moderate_income_units=housing_unit_body.moderate_income_units,
        middle_income_units=housing_unit_body.middle_income_units,
        other_income_units=housing_unit_body.other_income_units,
        studio_units=housing_unit_body.studio_units,
        one_br_units=housing_unit_body.one_br_units,
        two_br_units=housing_unit_body.two_br_units,
        three_br_units=housing_unit_body.three_br_units,
        four_br_units=housing_unit_body.four_br_units,
        five_br_units=housing_unit_body.five_br_units,
        six_br_units=housing_unit_body.six_br_units,
        unknown_br_units=housing_unit_body.unknown_br_units,
        counted_rental_units=housing_unit_body.counted_rental_units,
        counted_homeownership_units=housing_unit_body.counted_homeownership_units,
        all_counted_units=housing_unit_body.all_counted_units,
        total_units=housing_unit_body.total_units,
    )
