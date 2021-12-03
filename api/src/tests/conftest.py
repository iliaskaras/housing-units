import os

from application.authentication.models import JwtBody
from application.authentication.services import GetJWTService
from application.authentication.validators import JwtValidator
from application.infrastructure.configurations.enums import APIEnvironment
from application.infrastructure.configurations.models import API_ENVIRONMENT
from typing import List

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
            project_id='project id 1',
            street_name='street name test 1',
            borough='Queens',
            postcode=1,
            reporting_construction_type='construction type test 1',
            total_units=2
        ),
        HousingUnit(
            project_id='project id 2',
            street_name='street name test 2',
            borough='Brooklyn',
            postcode=2,
            reporting_construction_type='construction type test 2',
            total_units=4
        ),
        HousingUnit(
            project_id='project id 3',
            street_name='street name test 3',
            borough='Staten Island',
            postcode=3,
            reporting_construction_type='construction type test 3',
            total_units=6
        ),
        HousingUnit(
            project_id='project id 4',
            street_name='street name test 4',
            borough='Manhattan',
            postcode=4,
            reporting_construction_type='construction type test 4',
            total_units=8
        ),
        HousingUnit(
            project_id='project id 5',
            street_name='street name test 5',
            borough='Bronx',
            postcode=5,
            reporting_construction_type='construction type test 5',
            total_units=10
        ),
        HousingUnit(
            project_id='project id 6',
            street_name='street name test 1',
            borough='Queens',
            postcode=1,
            reporting_construction_type='construction type test 1',
            total_units=12
        ),
        HousingUnit(
            project_id='project id 7',
            street_name='street name test 2',
            borough='Brooklyn',
            postcode=2,
            reporting_construction_type='construction type test 2',
            total_units=14
        ),
        HousingUnit(
            project_id='project id 8',
            street_name='street name test 3',
            borough='Staten Island',
            postcode=3,
            reporting_construction_type='construction type test 3',
            total_units=16
        ),
        HousingUnit(
            project_id='project id 9',
            street_name='street name test 4',
            borough='Manhattan',
            postcode=4,
            reporting_construction_type='construction type test 4',
            total_units=18
        ),
        HousingUnit(
            project_id='project id 10',
            street_name='street name test 5',
            borough='Bronx',
            postcode=5,
            reporting_construction_type='construction type test 5',
            total_units=20
        ),
        HousingUnit(
            project_id='project id 11',
            street_name='street name test 1',
            borough='Queens',
            postcode=1,
            reporting_construction_type='construction type test 1',
            total_units=16
        ),
        HousingUnit(
            project_id='project id 12',
            street_name='street name test 1',
            borough='Queens',
            postcode=1,
            reporting_construction_type='construction type test 1',
            total_units=25
        ),
        HousingUnit(
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
