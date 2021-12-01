from sqlalchemy import Column, String, DateTime, Integer

from application.infrastructure.database.models import HousingUnitsDBBaseModel


class HBDBuilding(HousingUnitsDBBaseModel):
    project_id = Column(
        String,
        doc='The Project ID is a unique numeric identifier assigned to each project by HPD.',
        index=True,
        nullable=False
    )
    project_name = Column(
        String,
        doc='The Project Name is the name assigned to the project by HPD.'
    )
    project_start_date = Column(
        DateTime,
        doc='The Project Start Date is the date of the project loan or agreement closing.'
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
        nullable=False,
        index=True,
    )
    bbl = Column(
        Integer,
        doc='The BBL (Borough, Block, and Lot) is a unique identifier for each tax lot in the City.'
    )
    bin = Column(
        Integer,
        doc='The BIN (Building Identification Number) is a unique identifier for each building in the City.'
    )
    community_board = Column(
        String,
        doc='The Community Board field indicates the New York City Community District where the building is located.',
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
        Integer,
        doc='The Latitude and Longitude specify the location of the property on the earth’s surface. '
            'The coordinates provided are an estimate of the location based on the street segment and address range.'
    )
    longitude = Column(
        Integer,
        doc='The Latitude and Longitude specify the location of the property on the earth’s surface. '
            'The coordinates provided are an estimate of the location based on the street segment and address range.'
    )
    latitude_internal = Column(
        Integer,
        doc='The Latitude (Internal) and Longitude (Internal) specify the location of the property on the earth’s '
            'surface. The coordinates provided are of the internal centroid derived from the tax lot.'
    )
    longitude_internal = Column(
        Integer,
        doc='The Latitude (Internal) and Longitude (Internal) specify the location of the property on the earth’s '
            'surface. The coordinates provided are of the internal centroid derived from the tax lot.'
    )
    building_completion_date = Column(
        DateTime,
        doc='The Building Completion Date is the date the building was completed. The field is blank if the building '
            'has not completed.',
        nullable=False
    )
    reporting_construction_type = Column(
        String,
        doc='The Reporting Construction Type field indicates whether the building is categorized as '
            '‘new construction’ or ‘preservation’ in Housing New York statistics. Note that some preservation projects '
            'included here may not actually involve construction, because they extend the project’s regulatory '
            'restrictions but do not require rehabilitation.',
        nullable=False,
        index=True,
    )
    extended_affordability_status = Column(
        String,
        doc='The Extended Affordability Only field indicates whether the project is considered to be '
            'Extended Affordability. An extended affordability project involves no construction, but secures an '
            'extended or new regulatory agreement. All extended affordability projects have a ‘reporting construction '
            'type’ of ‘preservation.’',
    )
    prevailing_wage_status = Column(
        String,
        doc='The Prevailing Wage Status field indicates whether the project is subject to prevailing wage '
            'requirements, such as Davis Bacon.',
    )
    extremely_low_income_units = Column(
        Integer,
        doc='Extremely Low Income Units are units with rents that are affordable to households earning 0 to 30% '
            'of the area median income (AMI).',
        index=True,
    )
    very_low_income_units = Column(
        Integer,
        doc='Very Low Income Units are units with rents that are affordable to households earning 31 to 50% '
            'of the area median income (AMI).',
        index=True,
    )
    low_income_units = Column(
        Integer,
        doc='Low Income Units are units with rents that are affordable to households earning 51 to 80% of '
            'the area median income (AMI).',
        index=True,
    )
    moderate_income_units = Column(
        Integer,
        doc='Moderate Income Units are units with rents that are affordable to households earning 81 to 120% of the '
            'area median income (AMI).',
        index=True,
    )
    middle_income_units = Column(
        Integer,
        doc='Middle Income Units are units with rents that are affordable to households earning 121 to 165% '
            'of the area median income (AMI).',
        index=True,
    )
    other_income_units = Column(
        Integer,
        doc='Other Units are units reserved for building superintendents.',
        index=True,
    )
    studio_units = Column(
        Integer,
        doc='Studio Units are units with 0-bedrooms.',
        index=True,
    )
    _1_br_units = Column(
        Integer,
        doc='1-BR Units are units with 1-bedroom.',
        index=True,
    )
    _2_br_units = Column(
        Integer,
        doc='2-BR Units are units with 2-bedrooms.',
        index=True,
    )
    _3_br_units = Column(
        Integer,
        doc='3-BR Units are units with 3-bedrooms.',
        index=True,
    )
    _4_br_units = Column(
        Integer,
        doc='4-BR Units are units with 4-bedrooms.',
        index=True,
    )
    _5_br_units = Column(
        Integer,
        doc='5-BR Units are units with 5-bedrooms.',
        index=True,
    )
    _6_br_units = Column(
        Integer,
        doc='6-BR+ Units are units with 6-bedrooms or more.',
        index=True,
    )
    unknown_br_units = Column(
        Integer,
        doc='Unknown-BR Units are units with an unknown number of bedrooms.',
        index=True,
    )
    counted_rental_units = Column(
        Integer,
        doc='Counted Rental Units are the units in the building, counted toward the Housing New York plan, '
            'where assistance has been provided to landlords in exchange for a requirement for affordable units.'
    )
    counted_homeownership_units = Column(
        Integer,
        doc='Counted Homeownership Units are the units in the building, counted toward the Housing New York Plan, '
            'where assistance has been provided directly to homeowners.'
    )
    all_counted_units = Column(
        Integer,
        doc='The Counted Units field indicates the total number of affordable units, counted towards the Housing New '
            'York plan, that are in the building.',
        index=True,
    )
    total_units = Column(
        Integer,
        doc='The Total Units field indicates the total number of units, affordable and market rate, in each building.',
        index=True,
    )
