from pydantic import BaseModel, EmailStr
from pydantic.types import UUID, Enum


class UserResponse(BaseModel):
    uuid: UUID
    email: EmailStr
    is_active: bool
    user_group: Enum

    class Config:
        orm_mode = True

