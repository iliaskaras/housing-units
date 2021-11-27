from enum import Enum
from typing import List


class APIEnvironment(Enum):
    local = "local"
    test = "test"

    @classmethod
    def values(cls) -> List[str]:
        return [enum.value for enum in cls]
