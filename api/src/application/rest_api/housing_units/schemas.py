from typing import Optional, List

from fastapi import Query
from pydantic import BaseModel, Field
from pydantic.dataclasses import dataclass
from pydantic.json import UUID


@dataclass
class DataIngestionPostRequestBody:
    dataset_id: Optional[str] = 'hg8x-zxpr'
    reset_table: Optional[bool] = True


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
