from datetime import datetime

from beanie import Document, PydanticObjectId
from pydantic import BaseModel, ConfigDict, Field


class Library(Document):
    user_id: str
    title: str
    default: bool
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    papers: list[str] = []
    private: bool = False


class LibraryCreateInput(BaseModel):
    title: str
    private: bool = False


class LibraryUpdateInput(BaseModel):
    title: str = None
    private: bool = None


class LibraryPapersInput(BaseModel):
    paper_ids: set[str] = Field(..., min_length=1, max_length=500)


class LibraryPapersView(BaseModel):
    id: PydanticObjectId = Field(alias="_id")
    papers: list[str]


class LibraryLeanView(BaseModel):
    id: PydanticObjectId = Field(alias="_id")
    user_id: str
    title: str
    default: bool
    created_at: datetime
    updated_at: datetime
    private: bool
    num_papers: int

    class Settings:
        projection = {
            "user_id": 1,
            "title": 1,
            "default": 1,
            "created_at": 1,
            "updated_at": 1,
            "private": 1,
            "num_papers": {"$size": "$papers"},
        }


class LibraryResponse(BaseModel):
    id: PydanticObjectId = Field(alias="_id")
    user_id: str
    title: str
    default: bool
    created_at: datetime
    updated_at: datetime
    private: bool
    num_papers: int
    contains_paper: bool = None

    model_config = ConfigDict(populate_by_name=True)
