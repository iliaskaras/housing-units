from datetime import datetime
from typing import Optional, List

from fastapi import Query
from pydantic import BaseModel, Field
from pydantic.dataclasses import dataclass
from pydantic.json import UUID


@dataclass
class DataIngestionPostRequestBody:
    dataset_id: Optional[str] = 'hg8x-zxpr'
    reset_table: Optional[bool] = True


@dataclass
class HousingUnitPostRequestBody:
    one_br_units: Optional[int] = Field(default=0)
    two_br_units: Optional[int] = Field(default=0)
    three_br_units: Optional[int] = Field(default=0)
    four_br_units: Optional[int] = Field(default=0)
    five_br_units: Optional[int] = Field(default=0)
    six_br_units: Optional[int] = Field(default=0)
    project_name: Optional[str] = None
    project_id: str = Field()
    street_name: Optional[str] = None
    building_id: Optional[int] = Field(default=0)
    house_number: Optional[str] = None
    bbl: Optional[int] = Field(default=0)
    bin: Optional[int] = Field(default=0)
    community_board: Optional[str] = None
    council_district: Optional[int] = Field(default=0)
    census_tract: Optional[str] = None
    neighborhood_tabulation_area: Optional[str] = None
    latitude: Optional[float] = Field(default=0.0)
    longitude: Optional[float] = Field(default=0.0)
    latitude_internal: Optional[float] = Field(default=0.0)
    longitude_internal: Optional[float] = Field(default=0.0)
    extended_affordability_status: Optional[str] = None
    prevailing_wage_status: Optional[str] = None
    extremely_low_income_units: Optional[int] = Field(default=0)
    very_low_income_units: Optional[int] = Field(default=0)
    low_income_units: Optional[int] = Field(default=0)
    moderate_income_units: Optional[int] = Field(default=0)
    middle_income_units: Optional[int] = Field(default=0)
    other_income_units: Optional[int] = Field(default=0)
    studio_units: Optional[int] = Field(default=0)
    unknown_br_units: Optional[int] = Field(default=0)
    counted_rental_units: Optional[int] = Field(default=0)
    counted_homeownership_units: Optional[int] = Field(default=0)
    all_counted_units: Optional[int] = Field(default=0)
    borough: Optional[str] = Field(default=0)
    postcode: Optional[int] = Field(default=0)
    reporting_construction_type: Optional[str] = None
    total_units: Optional[int] = Field(default=0)
    project_start_date: Optional[datetime] = None
    project_completion_date: Optional[datetime] = None
    building_completion_date: Optional[datetime] = None


class HousingUnitResponse(BaseModel):
    id: Optional[UUID] = Field(alias="uuid")
    project_id: Optional[str]
    street_name: Optional[str]
    borough: Optional[str]
    postcode: Optional[int]
    construction_type: Optional[str] = Field(alias="reporting_construction_type")
    total_units: Optional[int]

    class Config:
        schema_extra = {
            "example": {
                "id": "e3b3326c-617a-4836-8fe0-3c17390f0bd4",
                "project_id": "44218",
                "borough": "Brooklyn",
                "street_name": "3 AVENUE",
                "postcode": "10035",
                "construction_type": "New Construction",
                "total_units": 5,
            }
        }
        orm_mode = True


class FullHousingUnitResponse(BaseModel):
    id: Optional[UUID] = Field(alias="uuid")
    project_id: Optional[str]
    street_name: Optional[str]
    borough: Optional[str]
    postcode: Optional[int]
    construction_type: Optional[str] = Field(alias="reporting_construction_type")
    total_units: Optional[int]
    project_name: Optional[str]
    project_start_date: Optional[datetime]
    project_completion_date: Optional[datetime]
    building_id: Optional[int]
    house_number: Optional[str]
    bbl: Optional[int]
    bin: Optional[int]
    community_board: Optional[str]
    council_district: Optional[int]
    census_tract: Optional[str]
    neighborhood_tabulation_area: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    latitude_internal: Optional[float]
    longitude_internal: Optional[float]
    building_completion_date: Optional[datetime]
    extended_affordability_status: Optional[str]
    prevailing_wage_status: Optional[str]
    extremely_low_income_units: Optional[int]
    very_low_income_units: Optional[int]
    low_income_units: Optional[int]
    moderate_income_units: Optional[int]
    middle_income_units: Optional[int]
    other_income_units: Optional[int]
    studio_units: Optional[int]
    one_br_units: Optional[int]
    two_br_units: Optional[int]
    three_br_units: Optional[int]
    four_br_units: Optional[int]
    five_br_units: Optional[int]
    six_br_units: Optional[int]
    unknown_br_units: Optional[int]
    counted_rental_units: Optional[int]
    counted_homeownership_units: Optional[int]
    all_counted_units: Optional[int]

    class Config:
        orm_mode = True


class FilterHousingUnits(BaseModel):
    housing_units: List[HousingUnitResponse] = Field(title='The filtered Housing Units.')
    total: int = Field(title='The total count of filtered Housing Units.')

    class Config:
        schema_extra = {
            "example": {
                "housing_units": [
                    {
                        "id": "e3b3326c-617a-4836-8fe0-3c17390f0bd4",
                        "project_id": "44218",
                        "borough": "Manhattan",
                        "street_name": "3 AVENUE",
                        "postcode": "10035",
                        "construction_type": "New Construction",
                        "total_units": 404,
                    },
                    {
                        "id": "e3b3326c-617a-4836-8fe0-3c17390f0bd4",
                        "project_id": "44218",
                        "borough": "Brooklyn",
                        "street_name": "RALPH AVENUE",
                        "postcode": None,
                        "construction_type": "New Construction",
                        "total_units": 10,
                    }
                ],
                "total": 2,
            }
        }


@dataclass
class FilterHousingUnitsGetRequestParameters:
    project_id: Optional[str] = Query(default=None)
    street_name: Optional[str] = Query(default=None)
    borough: Optional[str] = Query(default=None)
    postcode: Optional[int] = Query(default=None)
    construction_type: Optional[str] = Query(default=None)
    num_units_min: Optional[int] = Query(default=0, ge=0, title='Minimum number of building units.')
    num_units_max: Optional[int] = Query(default=1000, ge=0, title='Maximum number of building units.')
