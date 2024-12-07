from enum import Enum
from datetime import datetime
from typing import Annotated

from beanie import Document, Indexed, PydanticObjectId
from pydantic import BaseModel, Field, HttpUrl
import arxiv

from src.papers.adapters.arxiv_adapter import get_plain_id


class PaperSource(str, Enum):
    ARXIV = "arxiv"


class PaperBase(BaseModel):
    source: PaperSource
    source_id: str
    title: str
    pub_date: datetime
    authors: list[str]
    abstract: str
    doi: str | None = None
    likes: int = 0
    comments: int = 0


class Paper(Document, PaperBase):
    source_id: Annotated[str, Indexed(unique=True)]

    @classmethod
    def from_arxiv(cls, result: arxiv.Result):
        plain_id = get_plain_id(result)
        authors = [author.name for author in result.authors]
        return cls(
            id=PydanticObjectId(),
            source=PaperSource.ARXIV,
            source_id=plain_id,
            title=result.title,
            abstract=result.summary,
            pub_date=result.published,
            authors=authors,
            doi=result.doi,
        )


class PaperResponse(Paper):
    source_url: HttpUrl
    thumbnail_url: HttpUrl


class PaperIdView(BaseModel):
    id: PydanticObjectId = Field(alias="_id")
    source_id: str
    source: PaperSource
