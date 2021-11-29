from dataclasses import dataclass
from typing import Optional


@dataclass
class JwtBody:
    user_id: str
    group: str
    expires: Optional[float] = None
