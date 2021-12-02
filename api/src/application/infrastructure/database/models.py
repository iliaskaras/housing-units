from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base, declared_attr
import uuid


class DatabaseBaseModel(object):
    """
    Database Base model, adds common functionality to all the Database Tables.
    """

    @declared_attr
    def __tablename__(cls):
        # Since our class models are named in singular, we are making their table names in plural.
        return ''.join([cls.__name__.lower(), 's'])

    id = Column(Integer, primary_key=True)
    uuid = Column(UUID(as_uuid=True), unique=True, nullable=False, default=uuid.uuid4)


# The Base model that all the API tables should inherit from.
HousingUnitsDBBaseModel = declarative_base(cls=DatabaseBaseModel)
