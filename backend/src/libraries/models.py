from datetime import datetime

from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field


class Library(Document):
    user_id: str
    title: str
    default: bool
    created_at: datetime = Field(default_factory=datetime.now)
    papers: list[PydanticObjectId] = []
    private: bool = False


class LibraryCreateInput(BaseModel):
    title: str
    private: bool = False


class LibraryUpdateInput(BaseModel):
    title: str = None
    private: bool = None


class LibraryPapersInput(BaseModel):
    paper_ids: set[PydanticObjectId] = Field(..., min_length=1)
