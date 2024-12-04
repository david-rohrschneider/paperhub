from datetime import datetime

from beanie import Document
from pydantic import BaseModel

from src.papers.models import PaperSource


class Library(Document):
    user_id: str
    title: str
    default: bool
    created_at: datetime
    papers: list[str] = []
    private: bool = False


class LibraryCreateInput(BaseModel):
    title: str
    private: bool = False


class LibraryUpdateInput(BaseModel):
    title: str | None = None
    private: bool | None = None


class LibraryAddPaperInput(BaseModel):
    paper_id: str
    paper_source: PaperSource
