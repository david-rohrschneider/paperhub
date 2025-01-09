from typing import Generic, TypeVar
from pydantic import BaseModel


DataType = TypeVar("DataType")


class PaginatedResponse(BaseModel, Generic[DataType]):
    data: list[DataType]
    total: int
