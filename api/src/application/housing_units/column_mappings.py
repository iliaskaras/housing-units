from typing import Dict

"""
Dictionaries that helps optimizing our database table queries, by providing a way for avoiding the use of
sql functions directly on the table columns, for making the queries case insensitive.

The dictionaries are maps, and have as keys the lower case version of the table column value.

Note: This is just to highlight one of the ways that we can provide case insensitive implementation effectively.
Normally, in production systems, usually the client will have to choose the correct value (autocomplete for example)
and the need for case insensitive implementation no longer needed.
"""

# Maps the borough values that stored in the HousingUnits table, with their lowercase version.
# This is done for avoiding using the lower function directly on the column, and instead, use it
# on the provided value
UNIQUE_BOROUGH_MAPS: Dict[str, str] = {
    'queens': 'Queens',
    'brooklyn': 'Brooklyn',
    'staten island': 'Staten Island',
    'manhattan': 'Manhattan',
    'bronx': 'Bronx'
}
