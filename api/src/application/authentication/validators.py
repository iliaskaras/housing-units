from application.authentication.models import JwtBody
from application.infrastructure.error.errors import NoneArgumentError, ValidationError
from application.users.enums import Group


class JwtValidator:

    def validate(self, jwt_body: JwtBody) -> None:
        """
        Validates the JWT body token.

        :param jwt_body: The JWT body to validate.

        :raises ValidationError: If the jwt body does not have user_id, group or the group is
                not one of the correct ones.
                NoneArgumentError: If the jwt body is not provided.
        """
        if jwt_body is None:
            raise NoneArgumentError('A jwt body is required.')

        if not jwt_body.user_id:
            raise ValidationError(
                'User id is not included in the provided JWT body.'
            )

        if not jwt_body.group:
            raise ValidationError(
                'User group is not included in the provided JWT body.'
            )

        if jwt_body.group not in Group.values():
            raise ValidationError('User group is not supported')
