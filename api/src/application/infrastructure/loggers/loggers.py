import logging
import sys
from logging import Logger
from typing import Optional


class HousingUnitsAppLoggerFactory:
    LOGGER: Optional[Logger] = None

    @classmethod
    def initialize(cls) -> None:
        """
        Initialization of the application logger for the stderr channel logs.
        """
        logger = logging.getLogger('HOUSING UNITS API LOGGER')
        logger.setLevel(logging.INFO)

        stream_handler = logging.StreamHandler(sys.stderr)
        stream_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s")
        )
        logger.addHandler(stream_handler)

        cls.LOGGER = logger

    @classmethod
    def get(cls) -> Logger:
        if not cls.LOGGER:
            cls.initialize()

        return cls.LOGGER
