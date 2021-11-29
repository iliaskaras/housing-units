import time

import jwt

from application.authentication.models import JwtBody
from application.authentication.validators import JwtValidator
from application.infrastructure.configurations.models import Configuration
from application.infrastructure.error.errors import NoneArgumentError


class GetJWTService:

    def __init__(
            self,
            jwt_validator: JwtValidator,
            config: Configuration
    ) -> None:
        self.jwt_validator: JwtValidator = jwt_validator
        self.config: Configuration = config

    def apply(self, jwt_body: JwtBody = None) -> str:
        """
        Validates the provided jwt body we want to include into the encoded token
        and encodes the JWT token.

        :param jwt_body: The JWT body we want to include in the encoded token.

        :return: The encoded JWT in a string format.

        :raises NoneArgumentError: If the jwt body is not provided.
        """
        if jwt_body is None:
            raise NoneArgumentError('The jwt body is not provided.')

        self.jwt_validator.validate(jwt_body=jwt_body)

        return self._encode_jwt(jwt_body=jwt_body)

    def _encode_jwt(self, jwt_body: JwtBody) -> str:
        """
        Encodes the JWT token using the provided jwt body information.

        :param jwt_body: The JWT body we want to include in the encoded token.
        :return: The encoded JWT in a string format.
        """
        payload = {
            "user_id": jwt_body.user_id,
            "group": jwt_body.group,
            "expires": time.time() + 200
        }
        token: bytes = jwt.encode(payload, self.config.secret, algorithm=self.config.algorithm)

        return token.decode("utf-8")
