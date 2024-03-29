import math
from typing import Dict, Any

import numpy
from sqlalchemy import Column, String, DateTime, Integer, BigInteger, Float

from application.infrastructure.database.mappers import dataframe_timestamp_to_datetime
from application.infrastructure.database.models import HousingUnitsDBBaseModel


class HousingUnit(HousingUnitsDBBaseModel):
    project_id = Column(
        String,
        doc='The Project ID is a unique numeric identifier assigned to each project by HPD.',
        index=True,
        nullable=False
    )
    project_name = Column(
        String,
        doc='The Project Name is the name assigned to the project by HPD.',
        nullable=False
    )
    project_start_date = Column(
        DateTime,
        doc='The Project Start Date is the date of the project loan or agreement closing.',
        nullable=False
    )
    project_completion_date = Column(
        DateTime,
        doc='The Project Completion Date is the date that the last building in the project was completed. '
            'If the project has not yet completed, then the field is blank.',
    )
    building_id = Column(
        Integer,
        doc='The Building ID is a unique numeric identifier assigned to each building by HPD.'
    )
    house_number = Column(
        String,
        doc='The House Number is the street number in the building’s address. E.g., '
            'the house number is ‘100’ in ‘100 Gold Street.’',
    )
    street_name = Column(
        String,
        doc='The Street Name is the name of the street in the building’s address. E.g., '
            'the street name is ‘Gold Street’ in ‘100 Gold Street.’',
        nullable=False,
        index=True,
    )
    borough = Column(
        String,
        doc='The Borough is the borough where the building is located.',
        nullable=False,
        index=True,
    )
    postcode = Column(
        Integer,
        doc='Zip code',
        index=True,
    )
    bbl = Column(
        BigInteger,
        doc='The BBL (Borough, Block, and Lot) is a unique identifier for each tax lot in the City.'
    )
    bin = Column(
        Integer,
        doc='The BIN (Building Identification Number) is a unique identifier for each building in the City.'
    )
    community_board = Column(
        String,
        doc='The Community Board field indicates the New York City Community District where the building is located.',
        nullable=False
    )
    council_district = Column(
        Integer,
        doc='The Council District indicates the New York City Council District where the building is located.',
    )
    census_tract = Column(
        String,
        doc='The Census Tract indicates the 2010 U.S. Census Tract where the building is located.',
    )
    neighborhood_tabulation_area = Column(
        String,
        doc='The Neighborhood Tabulation Area indicates the New York City Neighborhood Tabulation Area where '
            'the building is located.',
    )
    latitude = Column(
        Float,
        doc='The Latitude and Longitude specify the location of the property on the earth’s surface. '
            'The coordinates provided are an estimate of the location based on the street segment and address range.'
    )
    longitude = Column(
        Float,
        doc='The Latitude and Longitude specify the location of the property on the earth’s surface. '
            'The coordinates provided are an estimate of the location based on the street segment and address range.'
    )
    latitude_internal = Column(
        Float,
        doc='The Latitude (Internal) and Longitude (Internal) specify the location of the property on the earth’s '
            'surface. The coordinates provided are of the internal centroid derived from the tax lot.'
    )
    longitude_internal = Column(
        Float,
        doc='The Latitude (Internal) and Longitude (Internal) specify the location of the property on the earth’s '
            'surface. The coordinates provided are of the internal centroid derived from the tax lot.'
    )
    building_completion_date = Column(
        DateTime,
        doc='The Building Completion Date is the date the building was completed. The field is blank if the building '
            'has not completed.'
    )
    reporting_construction_type = Column(
        String,
        doc='The Reporting Construction Type field indicates whether the building is categorized as '
            '‘new construction’ or ‘preservation’ in Housing New York statistics. Note that some preservation projects '
            'included here may not actually involve construction, because they extend the project’s regulatory '
            'restrictions but do not require rehabilitation.',
        index=True,
        nullable=False
    )
    extended_affordability_status = Column(
        String,
        doc='The Extended Affordability Only field indicates whether the project is considered to be '
            'Extended Affordability. An extended affordability project involves no construction, but secures an '
            'extended or new regulatory agreement. All extended affordability projects have a ‘reporting construction '
            'type’ of ‘preservation.’',
        nullable=False
    )
    prevailing_wage_status = Column(
        String,
        doc='The Prevailing Wage Status field indicates whether the project is subject to prevailing wage '
            'requirements, such as Davis Bacon.',
        nullable=False,
        default=0
    )
    extremely_low_income_units = Column(
        Integer,
        doc='Extremely Low Income Units are units with rents that are affordable to households earning 0 to 30% '
            'of the area median income (AMI).',
        index=True,
        nullable=False,
        default=0
    )
    very_low_income_units = Column(
        Integer,
        doc='Very Low Income Units are units with rents that are affordable to households earning 31 to 50% '
            'of the area median income (AMI).',
        index=True,
        nullable=False,
        default=0
    )
    low_income_units = Column(
        Integer,
        doc='Low Income Units are units with rents that are affordable to households earning 51 to 80% of '
            'the area median income (AMI).',
        index=True,
        nullable=False,
        default=0
    )
    moderate_income_units = Column(
        Integer,
        doc='Moderate Income Units are units with rents that are affordable to households earning 81 to 120% of the '
            'area median income (AMI).',
        index=True,
        nullable=False,
        default=0
    )
    middle_income_units = Column(
        Integer,
        doc='Middle Income Units are units with rents that are affordable to households earning 121 to 165% '
            'of the area median income (AMI).',
        index=True,
        nullable=False,
        default=0
    )
    other_income_units = Column(
        Integer,
        doc='Other Units are units reserved for building superintendents.',
        index=True,
        nullable=False,
        default=0
    )
    studio_units = Column(
        Integer,
        doc='Studio Units are units with 0-bedrooms.',
        index=True,
        nullable=False,
        default=0
    )
    one_br_units = Column(
        '_1_br_units',
        Integer,
        doc='1-BR Units are units with 1-bedroom.',
        index=True,
        nullable=False,
        default=0
    )
    two_br_units = Column(
        '_2_br_units',
        Integer,
        doc='2-BR Units are units with 2-bedrooms.',
        index=True,
        nullable=False,
        default=0
    )
    three_br_units = Column(
        '_3_br_units',
        Integer,
        doc='3-BR Units are units with 3-bedrooms.',
        index=True,
        nullable=False,
        default=0
    )
    four_br_units = Column(
        '_4_br_units',
        Integer,
        doc='4-BR Units are units with 4-bedrooms.',
        index=True,
        nullable=False,
        default=0
    )
    five_br_units = Column(
        '_5_br_units',
        Integer,
        doc='5-BR Units are units with 5-bedrooms.',
        index=True,
        nullable=False,
        default=0
    )
    six_br_units = Column(
        '_6_br_units',
        Integer,
        doc='6-BR+ Units are units with 6-bedrooms or more.',
        index=True,
        nullable=False,
        default=0
    )
    unknown_br_units = Column(
        Integer,
        doc='Unknown-BR Units are units with an unknown number of bedrooms.',
        index=True,
        nullable=False,
        default=0
    )
    counted_rental_units = Column(
        Integer,
        doc='Counted Rental Units are the units in the building, counted toward the Housing New York plan, '
            'where assistance has been provided to landlords in exchange for a requirement for affordable units.',
        nullable=False,
        default=0
    )
    counted_homeownership_units = Column(
        Integer,
        doc='Counted Homeownership Units are the units in the building, counted toward the Housing New York Plan, '
            'where assistance has been provided directly to homeowners.',
        nullable=False,
        default=0
    )
    all_counted_units = Column(
        Integer,
        doc='The Counted Units field indicates the total number of affordable units, counted towards the Housing New '
            'York plan, that are in the building.',
        index=True,
        nullable=False,
        default=0
    )
    total_units = Column(
        Integer,
        doc='The Total Units field indicates the total number of units, affordable and market rate, in each building.',
        index=True,
        nullable=False,
        default=0
    )

    @staticmethod
    def from_dict(dictionary: Dict[str, Any]) -> 'HousingUnit':
        """
        Maps the fields to their correct types, for being inserted correctly to the DB.
        The following maps are performed:
        1. Socrata's dates are mapped to datetime objects.
        2. String to integers, and strings to floats when the field is integer or float.
        3. NaN values to None.

        :param dictionary: Dictionary coming from the SocrataClient, which representing a single HousingUnit entry.

        :return: The HousingUnit with the field types corrected.
        """
        test = HousingUnit(
            project_id=dictionary['project_id'],
            project_name=dictionary['project_name'],
            project_start_date=dataframe_timestamp_to_datetime(dictionary['project_start_date']) if dictionary[
                                                                                                        'project_start_date'] is not numpy.nan else None,
            project_completion_date=dataframe_timestamp_to_datetime(dictionary['project_completion_date']) if
            dictionary['project_completion_date'] is not numpy.nan else None,
            building_id=int(dictionary['building_id']) if not math.isnan(dictionary['building_id']) else None,
            house_number=dictionary['house_number'],
            street_name=dictionary['street_name'],
            borough=dictionary['borough'],
            postcode=int(dictionary['postcode']) if not math.isnan(dictionary['postcode']) else None,
            bbl=int(dictionary['bbl']) if not math.isnan(dictionary['bbl']) else None,
            bin=int(dictionary['bin']) if not math.isnan(dictionary['bin']) else None,
            community_board=dictionary['community_board'],
            council_district=int(dictionary['building_id']) if not math.isnan(dictionary['building_id']) else None,
            census_tract=dictionary['census_tract'] if isinstance(dictionary['census_tract'], str) else None,
            neighborhood_tabulation_area=dictionary['neighborhood_tabulation_area'] if isinstance(
                dictionary['neighborhood_tabulation_area'], str) else None,
            latitude=dictionary['latitude'] if not math.isnan(dictionary['latitude']) else None,
            longitude=dictionary['longitude'] if not math.isnan(dictionary['longitude']) else None,
            latitude_internal=dictionary['latitude_internal'] if not math.isnan(
                dictionary['latitude_internal']) else None,
            longitude_internal=dictionary['longitude_internal'] if not math.isnan(
                dictionary['longitude_internal']) else None,
            building_completion_date=dataframe_timestamp_to_datetime(dictionary['building_completion_date']) if
            dictionary['building_completion_date'] is not numpy.nan else None,
            reporting_construction_type=dictionary['reporting_construction_type'],
            extended_affordability_status=dictionary['extended_affordability_status'],
            prevailing_wage_status=dictionary['prevailing_wage_status'],
            extremely_low_income_units=int(dictionary['extremely_low_income_units']) if not math.isnan(
                dictionary['extremely_low_income_units']) else None,
            very_low_income_units=int(dictionary['very_low_income_units']) if not math.isnan(
                dictionary['very_low_income_units']) else None,
            low_income_units=int(dictionary['low_income_units']) if not math.isnan(
                dictionary['low_income_units']) else None,
            moderate_income_units=int(dictionary['moderate_income_units']) if not math.isnan(
                dictionary['moderate_income_units']) else None,
            middle_income_units=int(dictionary['middle_income_units']) if not math.isnan(
                dictionary['middle_income_units']) else None,
            other_income_units=int(dictionary['other_income_units']) if not math.isnan(
                dictionary['other_income_units']) else None,
            studio_units=int(dictionary['studio_units']) if not math.isnan(dictionary['studio_units']) else None,
            one_br_units=int(dictionary['_1_br_units']) if not math.isnan(dictionary['_1_br_units']) else None,
            two_br_units=int(dictionary['_2_br_units']) if not math.isnan(dictionary['_2_br_units']) else None,
            three_br_units=int(dictionary['_3_br_units']) if not math.isnan(dictionary['_3_br_units']) else None,
            four_br_units=int(dictionary['_4_br_units']) if not math.isnan(dictionary['_4_br_units']) else None,
            five_br_units=int(dictionary['_5_br_units']) if not math.isnan(dictionary['_5_br_units']) else None,
            six_br_units=int(dictionary['_6_br_units']) if not math.isnan(dictionary['_6_br_units']) else None,
            unknown_br_units=int(dictionary['unknown_br_units']) if not math.isnan(
                dictionary['unknown_br_units']) else None,
            counted_rental_units=int(dictionary['counted_rental_units']) if not math.isnan(
                dictionary['counted_rental_units']) else None,
            counted_homeownership_units=int(dictionary['counted_homeownership_units']) if not math.isnan(
                dictionary['counted_homeownership_units']) else None,
            all_counted_units=int(dictionary['all_counted_units']) if not math.isnan(
                dictionary['all_counted_units']) else None,
            total_units=int(dictionary['total_units']) if not math.isnan(dictionary['total_units']) else None
        )
        return test

    def __eq__(self, other) -> bool:
        """
        Asserting equality between two different HousingUnit instances.

        :param other: The instance we want to compare with.

        :return: True if they are have equal fields false otherwise.
        """
        if isinstance(other, HousingUnit):
            return self.project_id == other.project_id \
                   and self.project_name == other.project_name \
                   and self.project_start_date == other.project_start_date \
                   and self.project_completion_date == other.project_completion_date \
                   and self.building_id == other.building_id \
                   and self.house_number == other.house_number \
                   and self.street_name == other.street_name \
                   and self.borough == other.borough \
                   and self.postcode == other.postcode \
                   and self.bbl == other.bbl \
                   and self.bin == other.bin \
                   and self.community_board == other.community_board \
                   and self.council_district == other.council_district \
                   and self.census_tract == other.census_tract \
                   and self.neighborhood_tabulation_area == other.neighborhood_tabulation_area \
                   and self.latitude == other.latitude \
                   and self.longitude == other.longitude \
                   and self.latitude_internal == other.latitude_internal \
                   and self.longitude_internal == other.longitude_internal \
                   and self.building_completion_date == other.building_completion_date \
                   and self.reporting_construction_type == other.reporting_construction_type \
                   and self.extended_affordability_status == other.extended_affordability_status \
                   and self.prevailing_wage_status == other.prevailing_wage_status \
                   and self.extremely_low_income_units == other.extremely_low_income_units \
                   and self.very_low_income_units == other.very_low_income_units \
                   and self.low_income_units == other.low_income_units \
                   and self.moderate_income_units == other.moderate_income_units \
                   and self.middle_income_units == other.middle_income_units \
                   and self.other_income_units == other.other_income_units \
                   and self.studio_units == other.studio_units \
                   and self.one_br_units == other.one_br_units \
                   and self.two_br_units == other.two_br_units \
                   and self.three_br_units == other.three_br_units \
                   and self.four_br_units == other.four_br_units \
                   and self.five_br_units == other.five_br_units \
                   and self.six_br_units == other.six_br_units \
                   and self.unknown_br_units == other.unknown_br_units \
                   and self.counted_rental_units == other.counted_rental_units \
                   and self.counted_homeownership_units == other.counted_homeownership_units \
                   and self.all_counted_units == other.all_counted_units \
                   and self.total_units == other.total_units

        return False
