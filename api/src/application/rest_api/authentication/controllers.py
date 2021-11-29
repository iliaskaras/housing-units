from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from application.rest_api.authentication.models import LoginPostRequestBody
from application.rest_api.authentication.schemas import AuthenticateJwtResponse
from application.users.container import UserContainer
from application.users.services import LoginUserService

router = APIRouter()


@router.post("/login", response_model=AuthenticateJwtResponse)
@inject
async def login(
        login_post_request_body: LoginPostRequestBody,
        login_user_service: LoginUserService = Depends(Provide[UserContainer.login_user_service]),
):
    """
    Controller for authenticating the users.

    :param login_post_request_body: The post request body required.
    :param login_user_service: The login server which will authenticate the user.

    :return: The encoded JWT response.
    """
    return await login_user_service.apply(
        email=login_post_request_body.email, password=login_post_request_body.password
    )
