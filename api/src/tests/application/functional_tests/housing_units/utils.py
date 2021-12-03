from typing import Any, Dict, List


def get_cleaned_housing_units_response(housing_units: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Cleans the housing units by removing the fields that cannot be checked on equality operation, like uuid.

    :param housing_units: A list of dictionaries representing the housing units.

    :return: The cleaned list of dictionaries representing the housing units.
    """
    for item in housing_units:
        item.pop('uuid')

    return housing_units
