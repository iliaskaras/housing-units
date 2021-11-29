from pydantic import BaseModel


class AuthenticateJwtResponse(BaseModel):
    access_token: str
