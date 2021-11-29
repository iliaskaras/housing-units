from typing import List

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from application.rest_api.users.schemas import UserResponse
from application.users.container import UserContainer
from application.users.services import GetActiveUsersService

router = APIRouter()


@router.get("/active-users", response_model=List[UserResponse])
@inject
async def get_active_users(
        user_service: GetActiveUsersService = Depends(Provide[UserContainer.get_active_users_service]),
):
    """
    Controller for returning all the active users.

    :param user_service: The service that used to return all the active users.

    :return: All the active users.
    """
    return await user_service.apply()
