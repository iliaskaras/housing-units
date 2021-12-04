import pytest
from fastapi.testclient import TestClient
from tests.application.functional_tests.housing_units.utils import get_cleaned_housing_units_response

from application.main import app

client = TestClient(app)


@pytest.mark.asyncio
async def test_filter_housing_units_get_request(
        populate_users, populate_housing_units, stub_housing_units, admin_jwt_token
):
    response = client.get("/housing-units", headers={"Authorization": "Bearer {}".format(admin_jwt_token)})
    assert response.status_code == 200
    response_json = response.json()
    total: int = response_json.get('total')
    assert total == len(stub_housing_units)
    housing_units = get_cleaned_housing_units_response(response_json.get('housing_units'))
    assert housing_units == [
        {
            'project_id': 'project id 1', 'street_name': 'street name test 1', 'borough': 'Queens', 'postcode': 1,
            'reporting_construction_type': 'construction type test 1', 'total_units': 2
        },
        {
            'project_id': 'project id 2', 'street_name': 'street name test 2', 'borough': 'Brooklyn', 'postcode': 2,
            'reporting_construction_type': 'construction type test 2', 'total_units': 4
        },
        {
            'project_id': 'project id 3', 'street_name': 'street name test 3', 'borough': 'Staten Island',
            'postcode': 3, 'reporting_construction_type': 'construction type test 3', 'total_units': 6
        },
        {
            'project_id': 'project id 4', 'street_name': 'street name test 4', 'borough': 'Manhattan', 'postcode': 4,
            'reporting_construction_type': 'construction type test 4', 'total_units': 8
        },
        {
            'project_id': 'project id 5', 'street_name': 'street name test 5', 'borough': 'Bronx', 'postcode': 5,
            'reporting_construction_type': 'construction type test 5', 'total_units': 10
        },
        {
            'project_id': 'project id 6', 'street_name': 'street name test 6', 'borough': 'Queens', 'postcode': 1,
            'reporting_construction_type': 'construction type test 6', 'total_units': 12
        },
        {
            'project_id': 'project id 7', 'street_name': 'street name test 7', 'borough': 'Brooklyn', 'postcode': 2,
            'reporting_construction_type': 'construction type test 7', 'total_units': 14
        },
        {
            'project_id': 'project id 11', 'street_name': 'street name test 11', 'borough': 'Queens', 'postcode': 1,
            'reporting_construction_type': 'construction type test 11', 'total_units': 16
        },
        {
            'project_id': 'project id 8', 'street_name': 'street name test 8', 'borough': 'Staten Island',
            'postcode': 3, 'reporting_construction_type': 'construction type test 8', 'total_units': 16
        },
        {
            'project_id': 'project id 9', 'street_name': 'street name test 9', 'borough': 'Manhattan', 'postcode': 4,
            'reporting_construction_type': 'construction type test 9', 'total_units': 18
        },
        {
            'project_id': 'project id 10', 'street_name': 'street name test 10', 'borough': 'Bronx', 'postcode': 5,
            'reporting_construction_type': 'construction type test 10', 'total_units': 20
        },
        {
            'project_id': 'project id 13', 'street_name': 'street name test 13', 'borough': 'Queens', 'postcode': 1,
            'reporting_construction_type': 'construction type test 13', 'total_units': 25
        },
        {
            'project_id': 'project id 12', 'street_name': 'street name test 12', 'borough': 'Queens', 'postcode': 1,
            'reporting_construction_type': 'construction type test 12', 'total_units': 25
        }
    ]


@pytest.mark.asyncio
async def test_filter_housing_units_get_request_called_by_customer(
        populate_users, populate_housing_units, stub_housing_units, customer_jwt_token
):
    response = client.get(
        "/housing-units?street_name=street name test 5&num_units_min=10",
        headers={"Authorization": "Bearer {}".format(customer_jwt_token)},
    )
    assert response.status_code == 200
    response_json = response.json()
    total: int = response_json.get('total')
    assert total == 1
    housing_units = get_cleaned_housing_units_response(response_json.get('housing_units'))
    assert housing_units == [
        {
            'project_id': 'project id 5',
            'street_name': 'street name test 5', 'borough': 'Bronx', 'postcode': 5,
            'reporting_construction_type': 'construction type test 5', 'total_units': 10
        }
    ]


@pytest.mark.asyncio
async def test_filter_housing_units_get_request_called_by_admin(
        populate_users, populate_housing_units, stub_housing_units, admin_jwt_token
):
    response = client.get(
        "/housing-units?street_name=street name test 5&num_units_min=10",
        headers={"Authorization": "Bearer {}".format(admin_jwt_token)},
    )
    assert response.status_code == 200
    response_json = response.json()
    total: int = response_json.get('total')
    assert total == 1
    housing_units = get_cleaned_housing_units_response(response_json.get('housing_units'))
    assert housing_units == [
        {
            'project_id': 'project id 5',
            'street_name': 'street name test 5', 'borough': 'Bronx', 'postcode': 5,
            'reporting_construction_type': 'construction type test 5', 'total_units': 10
        }
    ]


@pytest.mark.asyncio
async def test_filter_housing_units_get_request_raise_authorization_error_when_jwt_not_provided(
        populate_users, populate_housing_units, stub_housing_units
):
    response = client.get(
        "/housing-units?street_name=street name test 5&num_units_min=15"
    )
    assert response.status_code == 403
    assert response.json() == {'detail': 'Not authenticated'}


@pytest.mark.asyncio
async def test_filter_housing_units_get_request_raise_error_when_num_units_min_is_greater_than_max(
        populate_users, populate_housing_units, stub_housing_units, admin_jwt_token
):
    response = client.get(
        "/housing-units?street_name=street name test 5&num_units_min=15&num_units_max=10",
        headers={"Authorization": "Bearer {}".format(admin_jwt_token)},
    )
    assert response.status_code == 400
    assert response.json() == {
        "Detail": "The provided number of maximum units can't be smaller than the number of minimum units",
        "Type": "ValidationError"
    }


@pytest.mark.asyncio
async def test_retrieve_housing_unit_get_request_called_by_customer(
        populate_users, populate_housing_units, stub_housing_units, customer_jwt_token
):
    response = client.get(
        "/housing-units/{}".format(stub_housing_units[0].uuid),
        headers={"Authorization": "Bearer {}".format(customer_jwt_token)}
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json == {
        'uuid': stub_housing_units[0].uuid,
        'project_id': 'project id 1', 'street_name': 'street name test 1', 'borough': 'Queens', 'postcode': 1,
        'reporting_construction_type': 'construction type test 1', 'total_units': 2, 'project_name': 'project name 1',
        'project_start_date': '2018-12-25T11:27:53', 'project_completion_date': None,
        'building_id': None, 'house_number': None, 'bbl': None, 'bin': None, 'community_board': 'community board 1',
        'council_district': None, 'census_tract': None, 'neighborhood_tabulation_area': None, 'latitude': None,
        'longitude': None, 'latitude_internal': None, 'longitude_internal': None, 'building_completion_date': None,
        'extended_affordability_status': 'extended affordability status 1',
        'prevailing_wage_status': 'prevailing wage status 1', 'extremely_low_income_units': 0,
        'very_low_income_units': 0, 'low_income_units': 0, 'moderate_income_units': 0, 'middle_income_units': 2,
        'other_income_units': 0, 'studio_units': 0, 'one_br_units': 1, 'two_br_units': 0, 'three_br_units': 1,
        'four_br_units': 0, 'five_br_units': 0, 'six_br_units': 0, 'unknown_br_units': 0, 'counted_rental_units': 1,
        'counted_homeownership_units': 1, 'all_counted_units': 2
    }


@pytest.mark.asyncio
async def test_retrieve_housing_unit_get_request_called_by_admin(
        populate_users, populate_housing_units, stub_housing_units, admin_jwt_token
):
    response = client.get(
        "/housing-units/{}".format(stub_housing_units[0].uuid),
        headers={"Authorization": "Bearer {}".format(admin_jwt_token)}
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json == {
        'uuid': stub_housing_units[0].uuid,
        'project_id': 'project id 1', 'street_name': 'street name test 1', 'borough': 'Queens', 'postcode': 1,
        'reporting_construction_type': 'construction type test 1', 'total_units': 2, 'project_name': 'project name 1',
        'project_start_date': '2018-12-25T11:27:53', 'project_completion_date': None,
        'building_id': None, 'house_number': None, 'bbl': None, 'bin': None, 'community_board': 'community board 1',
        'council_district': None, 'census_tract': None, 'neighborhood_tabulation_area': None, 'latitude': None,
        'longitude': None, 'latitude_internal': None, 'longitude_internal': None, 'building_completion_date': None,
        'extended_affordability_status': 'extended affordability status 1',
        'prevailing_wage_status': 'prevailing wage status 1', 'extremely_low_income_units': 0,
        'very_low_income_units': 0, 'low_income_units': 0, 'moderate_income_units': 0, 'middle_income_units': 2,
        'other_income_units': 0, 'studio_units': 0, 'one_br_units': 1, 'two_br_units': 0, 'three_br_units': 1,
        'four_br_units': 0, 'five_br_units': 0, 'six_br_units': 0, 'unknown_br_units': 0, 'counted_rental_units': 1,
        'counted_homeownership_units': 1, 'all_counted_units': 2
    }


@pytest.mark.asyncio
async def test_retrieve_housing_unit_get_request_raise_authorization_error_when_jwt_not_provided(
        populate_users, populate_housing_units, stub_housing_units
):
    response = client.get(
        "/housing-units/{}".format(stub_housing_units[0].uuid),
    )
    assert response.status_code == 403
    assert response.json() == {'detail': 'Not authenticated'}


@pytest.mark.asyncio
async def test_post_housing_unit_request_called_by_admin(
        populate_users, populate_housing_units, stub_housing_units, admin_jwt_token, full_housing_unit_request_body
):
    response = client.post(
        "/housing-units/",
        headers={"Authorization": "Bearer {}".format(admin_jwt_token)},
        json=full_housing_unit_request_body
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json.get('uuid', None)
    response_json.pop('uuid')

    assert response_json == full_housing_unit_request_body


@pytest.mark.asyncio
async def test_post_housing_unit_request_called_by_customer(
        populate_users, populate_housing_units, stub_housing_units, customer_jwt_token, full_housing_unit_request_body
):
    response = client.post(
        "/housing-units/",
        headers={"Authorization": "Bearer {}".format(customer_jwt_token)},
        json=full_housing_unit_request_body
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json.get('uuid', None)
    response_json.pop('uuid')

    assert response_json == full_housing_unit_request_body


@pytest.mark.asyncio
async def test_post_housing_unit_request_raise_authorization_error_when_jwt_not_provided(
        populate_users, populate_housing_units, stub_housing_units
):
    response = client.post(
        "/housing-units/",
    )
    assert response.status_code == 403
    assert response.json() == {'detail': 'Not authenticated'}


@pytest.mark.asyncio
async def test_post_housing_unit_request_raise_unprocessable_entity_errors(
        populate_users,
        populate_housing_units,
        stub_housing_units,
        admin_jwt_token,
        full_housing_unit_request_body
):
    # Remove project_id which is required.
    full_housing_unit_request_body.pop('project_id')
    # Add a wrong formatted date to date fields.
    full_housing_unit_request_body['project_completion_date'] = 'not_correct_date'
    full_housing_unit_request_body['building_completion_date'] = 'not_correct_date'
    full_housing_unit_request_body['project_start_date'] = 'not_correct_date'
    # Add string to integer and float fields.
    full_housing_unit_request_body['postcode'] = 'not_correct_integer_or_float'
    full_housing_unit_request_body['total_units'] = 'not_correct_integer_or_float'
    full_housing_unit_request_body['building_id'] = 'not_correct_integer_or_float'
    full_housing_unit_request_body['bbl'] = 'not_correct_integer_or_float'
    full_housing_unit_request_body['bin'] = 'not_correct_integer_or_float'
    full_housing_unit_request_body['council_district'] = 'not_correct_integer_or_float'
    full_housing_unit_request_body['latitude'] = 'not_correct_integer_or_float'
    full_housing_unit_request_body['longitude'] = 'not_correct_integer_or_float'
    full_housing_unit_request_body['latitude_internal'] = 'not_correct_integer_or_float'
    full_housing_unit_request_body['longitude_internal'] = 'not_correct_integer_or_float'
    full_housing_unit_request_body['extremely_low_income_units'] = 'not_correct_integer_or_float'
    full_housing_unit_request_body['very_low_income_units'] = 'not_correct_integer_or_float'
    full_housing_unit_request_body['low_income_units'] = 'not_correct_integer_or_float'
    full_housing_unit_request_body['moderate_income_units'] = 'not_correct_integer_or_float'
    full_housing_unit_request_body['middle_income_units'] = 'not_correct_integer_or_float'
    full_housing_unit_request_body['other_income_units'] = 'not_correct_integer_or_float'
    full_housing_unit_request_body['studio_units'] = 'not_correct_integer_or_float'
    full_housing_unit_request_body['one_br_units'] = 'not_correct_integer_or_float'
    full_housing_unit_request_body['unknown_br_units'] = 'not_correct_integer_or_float'
    full_housing_unit_request_body['counted_rental_units'] = 'not_correct_integer_or_float'
    full_housing_unit_request_body['counted_homeownership_units'] = 'not_correct_integer_or_float'
    full_housing_unit_request_body['all_counted_units'] = 'not_correct_integer_or_float'

    response = client.post(
        "/housing-units/",
        headers={"Authorization": "Bearer {}".format(admin_jwt_token)},
        json=full_housing_unit_request_body
    )
    assert response.status_code == 422

    assert response.json() == {
        'detail': [
            {'loc': ['body', 'one_br_units'], 'msg': 'value is not a valid integer', 'type': 'type_error.integer'},
            {'loc': ['body', 'project_id'], 'msg': 'field required', 'type': 'value_error.missing'},
            {'loc': ['body', 'building_id'], 'msg': 'value is not a valid integer', 'type': 'type_error.integer'},
            {'loc': ['body', 'bbl'], 'msg': 'value is not a valid integer', 'type': 'type_error.integer'},
            {'loc': ['body', 'bin'], 'msg': 'value is not a valid integer', 'type': 'type_error.integer'},
            {'loc': ['body', 'council_district'], 'msg': 'value is not a valid integer', 'type': 'type_error.integer'},
            {'loc': ['body', 'latitude'], 'msg': 'value is not a valid float', 'type': 'type_error.float'},
            {'loc': ['body', 'longitude'], 'msg': 'value is not a valid float', 'type': 'type_error.float'},
            {'loc': ['body', 'latitude_internal'], 'msg': 'value is not a valid float', 'type': 'type_error.float'},
            {'loc': ['body', 'longitude_internal'], 'msg': 'value is not a valid float', 'type': 'type_error.float'},
            {'loc': ['body', 'extremely_low_income_units'], 'msg': 'value is not a valid integer',
             'type': 'type_error.integer'},
            {'loc': ['body', 'very_low_income_units'], 'msg': 'value is not a valid integer',
             'type': 'type_error.integer'},
            {'loc': ['body', 'low_income_units'], 'msg': 'value is not a valid integer', 'type': 'type_error.integer'},
            {'loc': ['body', 'moderate_income_units'], 'msg': 'value is not a valid integer',
             'type': 'type_error.integer'},
            {'loc': ['body', 'middle_income_units'], 'msg': 'value is not a valid integer',
             'type': 'type_error.integer'},
            {'loc': ['body', 'other_income_units'], 'msg': 'value is not a valid integer',
             'type': 'type_error.integer'},
            {'loc': ['body', 'studio_units'], 'msg': 'value is not a valid integer', 'type': 'type_error.integer'},
            {'loc': ['body', 'unknown_br_units'], 'msg': 'value is not a valid integer', 'type': 'type_error.integer'},
            {'loc': ['body', 'counted_rental_units'], 'msg': 'value is not a valid integer',
             'type': 'type_error.integer'},
            {'loc': ['body', 'counted_homeownership_units'], 'msg': 'value is not a valid integer',
             'type': 'type_error.integer'},
            {'loc': ['body', 'all_counted_units'], 'msg': 'value is not a valid integer', 'type': 'type_error.integer'},
            {'loc': ['body', 'postcode'], 'msg': 'value is not a valid integer', 'type': 'type_error.integer'},
            {'loc': ['body', 'total_units'], 'msg': 'value is not a valid integer', 'type': 'type_error.integer'},
            {'loc': ['body', 'project_start_date'], 'msg': 'invalid datetime format', 'type': 'value_error.datetime'},
            {'loc': ['body', 'project_completion_date'], 'msg': 'invalid datetime format',
             'type': 'value_error.datetime'},
            {'loc': ['body', 'building_completion_date'], 'msg': 'invalid datetime format',
             'type': 'value_error.datetime'}
        ]
    }


@pytest.mark.asyncio
async def test_put_housing_unit_request_called_by_admin(
        populate_users, populate_housing_units, stub_housing_units, admin_jwt_token
):
    put_request_body = {
        "project_id": "44223",
        "street_name": "RALPH AVENUE TEST",
        "borough": "Brooklyn",
        "postcode": None,
        "reporting_construction_type": "New Construction TEST",
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

    response = client.put(
        "/housing-units/{}".format(stub_housing_units[0].uuid),
        headers={"Authorization": "Bearer {}".format(admin_jwt_token)},
        json=put_request_body
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json.get('uuid', None)
    response_json.pop('uuid')

    assert response_json == {
        'project_id': '44223', 'street_name': 'RALPH AVENUE TEST', 'borough': 'Brooklyn', 'postcode': None,
        'reporting_construction_type': 'New Construction TEST', 'total_units': 10,
        'project_name': 'ROCHESTER SUYDAM PHASE 1', 'project_start_date': '2021-06-30T00:00:00',
        'project_completion_date': None, 'building_id': 977564, 'house_number': '329/331', 'bbl': None,
        'bin': None, 'community_board': 'BK-03', 'council_district': 977564, 'census_tract': None,
        'neighborhood_tabulation_area': None, 'latitude': None, 'longitude': None, 'latitude_internal': None,
        'longitude_internal': None, 'building_completion_date': None,
        'extended_affordability_status': 'No', 'prevailing_wage_status': 'Non Prevailing Wage',
        'extremely_low_income_units': 0, 'very_low_income_units': 0, 'low_income_units': 0,
        'moderate_income_units': 10, 'middle_income_units': 0, 'other_income_units': 0, 'studio_units': 0,
        'one_br_units': 3, 'two_br_units': 7, 'three_br_units': 0, 'four_br_units': 0, 'five_br_units': 0,
        'six_br_units': 0, 'unknown_br_units': 0, 'counted_rental_units': 0, 'counted_homeownership_units': 10,
        'all_counted_units': 10
    }


@pytest.mark.asyncio
async def test_put_housing_unit_request_called_by_customer(
        populate_users, populate_housing_units, stub_housing_units, customer_jwt_token
):
    put_request_body = {
        "project_id": "44223",
        "street_name": "RALPH AVENUE TEST",
        "borough": "Brooklyn",
        "postcode": None,
        "reporting_construction_type": "New Construction TEST",
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

    response = client.put(
        "/housing-units/{}".format(stub_housing_units[0].uuid),
        headers={"Authorization": "Bearer {}".format(customer_jwt_token)},
        json=put_request_body
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json.get('uuid', None)
    response_json.pop('uuid')

    assert response_json == {
        'project_id': '44223', 'street_name': 'RALPH AVENUE TEST', 'borough': 'Brooklyn', 'postcode': None,
        'reporting_construction_type': 'New Construction TEST', 'total_units': 10,
        'project_name': 'ROCHESTER SUYDAM PHASE 1', 'project_start_date': '2021-06-30T00:00:00',
        'project_completion_date': None, 'building_id': 977564, 'house_number': '329/331', 'bbl': None,
        'bin': None, 'community_board': 'BK-03', 'council_district': 977564, 'census_tract': None,
        'neighborhood_tabulation_area': None, 'latitude': None, 'longitude': None, 'latitude_internal': None,
        'longitude_internal': None, 'building_completion_date': None,
        'extended_affordability_status': 'No', 'prevailing_wage_status': 'Non Prevailing Wage',
        'extremely_low_income_units': 0, 'very_low_income_units': 0, 'low_income_units': 0,
        'moderate_income_units': 10, 'middle_income_units': 0, 'other_income_units': 0, 'studio_units': 0,
        'one_br_units': 3, 'two_br_units': 7, 'three_br_units': 0, 'four_br_units': 0, 'five_br_units': 0,
        'six_br_units': 0, 'unknown_br_units': 0, 'counted_rental_units': 0, 'counted_homeownership_units': 10,
        'all_counted_units': 10
    }


@pytest.mark.asyncio
async def test_put_housing_unit_request_raise_authorization_error_when_jwt_not_provided(
        populate_users, populate_housing_units, stub_housing_units
):
    response = client.put(
        "/housing-units/{}".format(stub_housing_units[0].uuid),
    )
    assert response.status_code == 403
    assert response.json() == {'detail': 'Not authenticated'}


@pytest.mark.asyncio
async def test_put_housing_unit_request_raise_unprocessable_entity_errors(
        populate_users,
        populate_housing_units,
        stub_housing_units,
        admin_jwt_token,
        full_housing_unit_request_body
):
    # Remove project_id which is required.
    full_housing_unit_request_body.pop('project_id')
    # Add a wrong formatted date to date fields.
    full_housing_unit_request_body['project_completion_date'] = 'not_correct_date'
    full_housing_unit_request_body['building_completion_date'] = 'not_correct_date'
    full_housing_unit_request_body['project_start_date'] = 'not_correct_date'
    # Add string to integer and float fields.
    full_housing_unit_request_body['postcode'] = 'not_correct_integer_or_float'
    full_housing_unit_request_body['total_units'] = 'not_correct_integer_or_float'
    full_housing_unit_request_body['building_id'] = 'not_correct_integer_or_float'
    full_housing_unit_request_body['bbl'] = 'not_correct_integer_or_float'
    full_housing_unit_request_body['bin'] = 'not_correct_integer_or_float'
    full_housing_unit_request_body['council_district'] = 'not_correct_integer_or_float'
    full_housing_unit_request_body['latitude'] = 'not_correct_integer_or_float'
    full_housing_unit_request_body['longitude'] = 'not_correct_integer_or_float'
    full_housing_unit_request_body['latitude_internal'] = 'not_correct_integer_or_float'
    full_housing_unit_request_body['longitude_internal'] = 'not_correct_integer_or_float'
    full_housing_unit_request_body['extremely_low_income_units'] = 'not_correct_integer_or_float'
    full_housing_unit_request_body['very_low_income_units'] = 'not_correct_integer_or_float'
    full_housing_unit_request_body['low_income_units'] = 'not_correct_integer_or_float'
    full_housing_unit_request_body['moderate_income_units'] = 'not_correct_integer_or_float'
    full_housing_unit_request_body['middle_income_units'] = 'not_correct_integer_or_float'
    full_housing_unit_request_body['other_income_units'] = 'not_correct_integer_or_float'
    full_housing_unit_request_body['studio_units'] = 'not_correct_integer_or_float'
    full_housing_unit_request_body['one_br_units'] = 'not_correct_integer_or_float'
    full_housing_unit_request_body['unknown_br_units'] = 'not_correct_integer_or_float'
    full_housing_unit_request_body['counted_rental_units'] = 'not_correct_integer_or_float'
    full_housing_unit_request_body['counted_homeownership_units'] = 'not_correct_integer_or_float'
    full_housing_unit_request_body['all_counted_units'] = 'not_correct_integer_or_float'

    response = client.put(
        "/housing-units/{}".format(stub_housing_units[0].uuid),
        headers={"Authorization": "Bearer {}".format(admin_jwt_token)},
        json=full_housing_unit_request_body
    )
    assert response.status_code == 422

    assert response.json() == {
        'detail': [
            {'loc': ['body', 'one_br_units'], 'msg': 'value is not a valid integer', 'type': 'type_error.integer'},
            {'loc': ['body', 'project_id'], 'msg': 'field required', 'type': 'value_error.missing'},
            {'loc': ['body', 'building_id'], 'msg': 'value is not a valid integer', 'type': 'type_error.integer'},
            {'loc': ['body', 'bbl'], 'msg': 'value is not a valid integer', 'type': 'type_error.integer'},
            {'loc': ['body', 'bin'], 'msg': 'value is not a valid integer', 'type': 'type_error.integer'},
            {'loc': ['body', 'council_district'], 'msg': 'value is not a valid integer', 'type': 'type_error.integer'},
            {'loc': ['body', 'latitude'], 'msg': 'value is not a valid float', 'type': 'type_error.float'},
            {'loc': ['body', 'longitude'], 'msg': 'value is not a valid float', 'type': 'type_error.float'},
            {'loc': ['body', 'latitude_internal'], 'msg': 'value is not a valid float', 'type': 'type_error.float'},
            {'loc': ['body', 'longitude_internal'], 'msg': 'value is not a valid float', 'type': 'type_error.float'},
            {'loc': ['body', 'extremely_low_income_units'], 'msg': 'value is not a valid integer',
             'type': 'type_error.integer'},
            {'loc': ['body', 'very_low_income_units'], 'msg': 'value is not a valid integer',
             'type': 'type_error.integer'},
            {'loc': ['body', 'low_income_units'], 'msg': 'value is not a valid integer', 'type': 'type_error.integer'},
            {'loc': ['body', 'moderate_income_units'], 'msg': 'value is not a valid integer',
             'type': 'type_error.integer'},
            {'loc': ['body', 'middle_income_units'], 'msg': 'value is not a valid integer',
             'type': 'type_error.integer'},
            {'loc': ['body', 'other_income_units'], 'msg': 'value is not a valid integer',
             'type': 'type_error.integer'},
            {'loc': ['body', 'studio_units'], 'msg': 'value is not a valid integer', 'type': 'type_error.integer'},
            {'loc': ['body', 'unknown_br_units'], 'msg': 'value is not a valid integer', 'type': 'type_error.integer'},
            {'loc': ['body', 'counted_rental_units'], 'msg': 'value is not a valid integer',
             'type': 'type_error.integer'},
            {'loc': ['body', 'counted_homeownership_units'], 'msg': 'value is not a valid integer',
             'type': 'type_error.integer'},
            {'loc': ['body', 'all_counted_units'], 'msg': 'value is not a valid integer', 'type': 'type_error.integer'},
            {'loc': ['body', 'postcode'], 'msg': 'value is not a valid integer', 'type': 'type_error.integer'},
            {'loc': ['body', 'total_units'], 'msg': 'value is not a valid integer', 'type': 'type_error.integer'},
            {'loc': ['body', 'project_start_date'], 'msg': 'invalid datetime format', 'type': 'value_error.datetime'},
            {'loc': ['body', 'project_completion_date'], 'msg': 'invalid datetime format',
             'type': 'value_error.datetime'},
            {'loc': ['body', 'building_completion_date'], 'msg': 'invalid datetime format',
             'type': 'value_error.datetime'}
        ]
    }
