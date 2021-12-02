from pydantic import BaseModel
from pydantic.dataclasses import dataclass


class AuthenticateJwtResponse(BaseModel):
    access_token: str


@dataclass
class LoginPostRequestBody:
    email: str
    password: str
