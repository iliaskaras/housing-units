import os

import uuid

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
    housing_units: List[HousingUnit] = [
        HousingUnit(
            uuid=str(uuid.uuid4()),
            project_id='project id 1',
            street_name='street name test 1',
            borough='Queens',
            postcode=1,
            reporting_construction_type='construction type test 1',
            total_units=2
        ),
        HousingUnit(
            uuid=str(uuid.uuid4()),
            project_id='project id 2',
            street_name='street name test 2',
            borough='Brooklyn',
            postcode=2,
            reporting_construction_type='construction type test 2',
            total_units=4
        ),
        HousingUnit(
            uuid=str(uuid.uuid4()),
            project_id='project id 3',
            street_name='street name test 3',
            borough='Staten Island',
            postcode=3,
            reporting_construction_type='construction type test 3',
            total_units=6
        ),
        HousingUnit(
            uuid=str(uuid.uuid4()),
            project_id='project id 4',
            street_name='street name test 4',
            borough='Manhattan',
            postcode=4,
            reporting_construction_type='construction type test 4',
            total_units=8
        ),
        HousingUnit(
            uuid=str(uuid.uuid4()),
            project_id='project id 5',
            street_name='street name test 5',
            borough='Bronx',
            postcode=5,
            reporting_construction_type='construction type test 5',
            total_units=10
        ),
        HousingUnit(
            uuid=str(uuid.uuid4()),
            project_id='project id 6',
            street_name='street name test 1',
            borough='Queens',
            postcode=1,
            reporting_construction_type='construction type test 1',
            total_units=12
        ),
        HousingUnit(
            uuid=str(uuid.uuid4()),
            project_id='project id 7',
            street_name='street name test 2',
            borough='Brooklyn',
            postcode=2,
            reporting_construction_type='construction type test 2',
            total_units=14
        ),
        HousingUnit(
            uuid=str(uuid.uuid4()),
            project_id='project id 8',
            street_name='street name test 3',
            borough='Staten Island',
            postcode=3,
            reporting_construction_type='construction type test 3',
            total_units=16
        ),
        HousingUnit(
            uuid=str(uuid.uuid4()),
            project_id='project id 9',
            street_name='street name test 4',
            borough='Manhattan',
            postcode=4,
            reporting_construction_type='construction type test 4',
            total_units=18
        ),
        HousingUnit(
            uuid=str(uuid.uuid4()),
            project_id='project id 10',
            street_name='street name test 5',
            borough='Bronx',
            postcode=5,
            reporting_construction_type='construction type test 5',
            total_units=20
        ),
        HousingUnit(
            uuid=str(uuid.uuid4()),
            project_id='project id 11',
            street_name='street name test 1',
            borough='Queens',
            postcode=1,
            reporting_construction_type='construction type test 1',
            total_units=16
        ),
        HousingUnit(
            uuid=str(uuid.uuid4()),
            project_id='project id 12',
            street_name='street name test 1',
            borough='Queens',
            postcode=1,
            reporting_construction_type='construction type test 1',
            total_units=25
        ),
        HousingUnit(
            uuid=str(uuid.uuid4()),
            project_id='project id 12',
            street_name='street name test 1',
            borough='Queens',
            postcode=1,
            reporting_construction_type='construction type test 1',
            total_units=25
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
        "street_name": "RALPH AVENUE TEST",
        "borough": "Brooklyn",
        "postcode": 11233,
        "reporting_construction_type": "New Construction",
        "total_units": 13,
        "project_name": "ROCHESTER SUYDAM PHASE 1",
        "project_start_date": "2021-06-30T00:00:00",
        "project_completion_date": None,
        "building_id": 927737,
        "house_number": "335",
        "bbl": 3015560003,
        "bin": None,
        "community_board": "BK-03",
        "council_district": 927737,
        "census_tract": "301",
        "neighborhood_tabulation_area": "BK79",
        "latitude": 40.677644,
        "longitude": -73.921745,
        "latitude_internal": 40.67747,
        "longitude_internal": -73.921492,
        "building_completion_date": None,
        "extended_affordability_status": "No",
        "prevailing_wage_status": "Non Prevailing Wage",
        "extremely_low_income_units": 0,
        "very_low_income_units": 0,
        "low_income_units": 0,
        "moderate_income_units": 13,
        "middle_income_units": 0,
        "other_income_units": 0,
        "studio_units": 0,
        "one_br_units": 2,
        "unknown_br_units": 0,
        "counted_rental_units": 0,
        "counted_homeownership_units": 13,
        "all_counted_units": 13
    }
