import time

import jwt

from application.authentication.models import JwtBody
from application.infrastructure.configurations.models import Configuration
from application.users.enums import Group
from typing import List
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


class BearerJWTAuthorizationService(HTTPBearer):

    def __init__(self, auto_error: bool = True, permission_groups: List[Group] = []):
        super(BearerJWTAuthorizationService, self).__init__(auto_error=auto_error)
        self.config: Configuration = Configuration.get()
        self.permission_groups: List[str] = [group.value for group in permission_groups]

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(BearerJWTAuthorizationService, self).__call__(request)

        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")

            self.verify_jwt(jwt_token=credentials.credentials)

            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwt_token: str) -> dict:
        try:
            decoded_jwt_token: JwtBody = self.decode_jwt(jwt_token)

        except Exception:
            raise HTTPException(status_code=403, detail="Invalid token.")

        if decoded_jwt_token.group not in self.permission_groups:
            raise HTTPException(status_code=403, detail="You can't access this resource.")

    def decode_jwt(self, token: str) -> JwtBody:
        decoded_token = jwt.decode(token, self.config.secret, algorithms=[self.config.algorithm])
        if decoded_token["expires"] < time.time():
            raise HTTPException(status_code=403, detail="Token expired.")
        return JwtBody(**decoded_token)
