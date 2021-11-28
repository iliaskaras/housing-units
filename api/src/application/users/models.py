from sqlalchemy import Column, String, Boolean, Enum

from application.infrastructure.database.models import HousingUnitsDBBaseModel
from application.users.enums import Group


class User(HousingUnitsDBBaseModel):

    email = Column(String, unique=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    user_group = Column(Enum(Group, validate_strings=True), nullable=False)
