from datetime import datetime

import numpy


def dataframe_timestamp_to_datetime(timestamp: str) -> datetime:
    """
    Maps a dataframe string timestamp to its datetime version.

    :param timestamp: A DataFrame string timestamp.

    :return: The datetime.
    """
    return datetime.utcfromtimestamp(numpy.datetime64(timestamp, 's').astype(int))
