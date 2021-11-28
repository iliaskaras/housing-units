from typing import List

from enum import Enum


class Group(Enum):
    admin = 'admin'
    customer = 'customer'

    @classmethod
    def values(cls) -> List[str]:
        return [member.value for member in cls]
