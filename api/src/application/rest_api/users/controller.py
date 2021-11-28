from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from application.users.container import UserContainer
from application.users.services import UserService

router = APIRouter()


@router.get("/users")
@inject
async def get_users(
        user_service: UserService = Depends(Provide[UserContainer.user_service]),
):
    return user_service.get_users()
