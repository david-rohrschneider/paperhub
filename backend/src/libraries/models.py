from datetime import datetime

from beanie import Document
from pydantic import BaseModel, Field

from src.papers.models import PaperLeanResponse


class Library(Document):
    user_id: str
    title: str
    default: bool
    created_at: datetime = Field(default_factory=datetime.now)
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


class LibraryResponse(Library):
    papers: list[PaperLeanResponse]
