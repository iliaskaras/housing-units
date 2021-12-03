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
            'project_id': 'project id 1',
            'street_name': 'street name test 1', 'borough': 'Queens', 'postcode': 1,
            'reporting_construction_type': 'construction type test 1', 'total_units': 2
        },
        {
            'project_id': 'project id 2',
            'street_name': 'street name test 2', 'borough': 'Brooklyn', 'postcode': 2,
            'reporting_construction_type': 'construction type test 2', 'total_units': 4
        },
        {
            'project_id': 'project id 3',
            'street_name': 'street name test 3', 'borough': 'Staten Island', 'postcode': 3,
            'reporting_construction_type': 'construction type test 3', 'total_units': 6
        },
        {
            'project_id': 'project id 4',
            'street_name': 'street name test 4', 'borough': 'Manhattan', 'postcode': 4,
            'reporting_construction_type': 'construction type test 4', 'total_units': 8
        },
        {
            'project_id': 'project id 5',
            'street_name': 'street name test 5', 'borough': 'Bronx', 'postcode': 5,
            'reporting_construction_type': 'construction type test 5', 'total_units': 10
        },
        {
            'project_id': 'project id 6',
            'street_name': 'street name test 1', 'borough': 'Queens', 'postcode': 1,
            'reporting_construction_type': 'construction type test 1', 'total_units': 12
        },
        {
            'project_id': 'project id 7',
            'street_name': 'street name test 2', 'borough': 'Brooklyn', 'postcode': 2,
            'reporting_construction_type': 'construction type test 2', 'total_units': 14
        },
        {
            'project_id': 'project id 11',
            'street_name': 'street name test 1', 'borough': 'Queens', 'postcode': 1,
            'reporting_construction_type': 'construction type test 1', 'total_units': 16
        },
        {
            'project_id': 'project id 8',
            'street_name': 'street name test 3', 'borough': 'Staten Island', 'postcode': 3,
            'reporting_construction_type': 'construction type test 3', 'total_units': 16
        },
        {
            'project_id': 'project id 9',
            'street_name': 'street name test 4', 'borough': 'Manhattan', 'postcode': 4,
            'reporting_construction_type': 'construction type test 4', 'total_units': 18
        },
        {
            'project_id': 'project id 10',
            'street_name': 'street name test 5', 'borough': 'Bronx', 'postcode': 5,
            'reporting_construction_type': 'construction type test 5', 'total_units': 20
        },
        {
            'project_id': 'project id 12',
            'street_name': 'street name test 1', 'borough': 'Queens', 'postcode': 1,
            'reporting_construction_type': 'construction type test 1', 'total_units': 25
        },
        {
            'project_id': 'project id 12',
            'street_name': 'street name test 1', 'borough': 'Queens', 'postcode': 1,
            'reporting_construction_type': 'construction type test 1', 'total_units': 25
        }
    ]


@pytest.mark.asyncio
async def test_filter_housing_units_get_request_with_parameters(
        populate_users, populate_housing_units, stub_housing_units, admin_jwt_token
):
    response = client.get(
        "/housing-units?street_name=street name test 5&num_units_min=15",
        headers={"Authorization": "Bearer {}".format(admin_jwt_token)},
    )
    assert response.status_code == 200
    response_json = response.json()
    total: int = response_json.get('total')
    assert total == 1
    housing_units = get_cleaned_housing_units_response(response_json.get('housing_units'))
    assert housing_units == [
        {
            'project_id': 'project id 10',
            'street_name': 'street name test 5', 'borough': 'Bronx', 'postcode': 5,
            'reporting_construction_type': 'construction type test 5', 'total_units': 20
        },
    ]


@pytest.mark.asyncio
async def test_filter_housing_units_get_request_called_by_customer(
        populate_users, populate_housing_units, stub_housing_units, customer_jwt_token
):
    response = client.get(
        "/housing-units?street_name=street name test 5&num_units_min=15",
        headers={"Authorization": "Bearer {}".format(customer_jwt_token)},
    )
    assert response.status_code == 200
    response_json = response.json()
    total: int = response_json.get('total')
    assert total == 1
    housing_units = get_cleaned_housing_units_response(response_json.get('housing_units'))
    assert housing_units == [
        {
            'project_id': 'project id 10',
            'street_name': 'street name test 5', 'borough': 'Bronx', 'postcode': 5,
            'reporting_construction_type': 'construction type test 5', 'total_units': 20
        },
    ]


@pytest.mark.asyncio
async def test_filter_housing_units_get_request_called_by_admin(
        populate_users, populate_housing_units, stub_housing_units, admin_jwt_token
):
    response = client.get(
        "/housing-units?street_name=street name test 5&num_units_min=15",
        headers={"Authorization": "Bearer {}".format(admin_jwt_token)},
    )
    assert response.status_code == 200
    response_json = response.json()
    total: int = response_json.get('total')
    assert total == 1
    housing_units = get_cleaned_housing_units_response(response_json.get('housing_units'))
    assert housing_units == [
        {
            'project_id': 'project id 10',
            'street_name': 'street name test 5', 'borough': 'Bronx', 'postcode': 5,
            'reporting_construction_type': 'construction type test 5', 'total_units': 20
        },
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
async def test_retrieve_housing_unit_get_request(
        populate_users, populate_housing_units, stub_housing_units, admin_jwt_token
):
    response = client.get(
        "/housing-units/{}".format(stub_housing_units[0].uuid),
        headers={"Authorization": "Bearer {}".format(admin_jwt_token)}
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json == {
        'all_counted_units': None,
        'bbl': None,
        'bin': None,
        'borough': 'Queens',
        'building_completion_date': None,
        'building_id': None,
        'census_tract': None,
        'community_board': None,
        'council_district': None,
        'counted_homeownership_units': None,
        'counted_rental_units': None,
        'extended_affordability_status': None,
        'extremely_low_income_units': None,
        'five_br_units': None,
        'four_br_units': None,
        'house_number': None,
        'latitude': None,
        'latitude_internal': None,
        'longitude': None,
        'longitude_internal': None,
        'low_income_units': None,
        'middle_income_units': None,
        'moderate_income_units': None,
        'neighborhood_tabulation_area': None,
        'one_br_units': None,
        'other_income_units': None,
        'postcode': 1,
        'prevailing_wage_status': None,
        'project_completion_date': None,
        'project_id': 'project id 1',
        'project_name': None,
        'project_start_date': None,
        'reporting_construction_type': 'construction type test 1',
        'six_br_units': None,
        'street_name': 'street name test 1',
        'studio_units': None,
        'three_br_units': None,
        'total_units': 2,
        'two_br_units': None,
        'unknown_br_units': None,
        'uuid': stub_housing_units[0].uuid,
        'very_low_income_units': None
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
        'all_counted_units': None,
        'bbl': None,
        'bin': None,
        'borough': 'Queens',
        'building_completion_date': None,
        'building_id': None,
        'census_tract': None,
        'community_board': None,
        'council_district': None,
        'counted_homeownership_units': None,
        'counted_rental_units': None,
        'extended_affordability_status': None,
        'extremely_low_income_units': None,
        'five_br_units': None,
        'four_br_units': None,
        'house_number': None,
        'latitude': None,
        'latitude_internal': None,
        'longitude': None,
        'longitude_internal': None,
        'low_income_units': None,
        'middle_income_units': None,
        'moderate_income_units': None,
        'neighborhood_tabulation_area': None,
        'one_br_units': None,
        'other_income_units': None,
        'postcode': 1,
        'prevailing_wage_status': None,
        'project_completion_date': None,
        'project_id': 'project id 1',
        'project_name': None,
        'project_start_date': None,
        'reporting_construction_type': 'construction type test 1',
        'six_br_units': None,
        'street_name': 'street name test 1',
        'studio_units': None,
        'three_br_units': None,
        'total_units': 2,
        'two_br_units': None,
        'unknown_br_units': None,
        'uuid': stub_housing_units[0].uuid,
        'very_low_income_units': None
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
        'all_counted_units': None,
        'bbl': None,
        'bin': None,
        'borough': 'Queens',
        'building_completion_date': None,
        'building_id': None,
        'census_tract': None,
        'community_board': None,
        'council_district': None,
        'counted_homeownership_units': None,
        'counted_rental_units': None,
        'extended_affordability_status': None,
        'extremely_low_income_units': None,
        'five_br_units': None,
        'four_br_units': None,
        'house_number': None,
        'latitude': None,
        'latitude_internal': None,
        'longitude': None,
        'longitude_internal': None,
        'low_income_units': None,
        'middle_income_units': None,
        'moderate_income_units': None,
        'neighborhood_tabulation_area': None,
        'one_br_units': None,
        'other_income_units': None,
        'postcode': 1,
        'prevailing_wage_status': None,
        'project_completion_date': None,
        'project_id': 'project id 1',
        'project_name': None,
        'project_start_date': None,
        'reporting_construction_type': 'construction type test 1',
        'six_br_units': None,
        'street_name': 'street name test 1',
        'studio_units': None,
        'three_br_units': None,
        'total_units': 2,
        'two_br_units': None,
        'unknown_br_units': None,
        'uuid': stub_housing_units[0].uuid,
        'very_low_income_units': None
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
