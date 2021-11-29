from pydantic.dataclasses import dataclass


@dataclass
class LoginPostRequestBody:
    email: str
    password: str
