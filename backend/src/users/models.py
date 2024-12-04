from datetime import datetime
from typing import Annotated
from enum import Enum

from beanie import Document, Indexed
from pydantic import BaseModel, EmailStr

from src.papers.adapters.arxiv_adapter import ArxivCategory


class UserLinks(BaseModel):
    """User social and academic links."""

    orcid: str | None = None
    google_scholar: str | None = None
    researchgate: str | None = None
    linkedin: str | None = None


class UserTitle(str, Enum):
    """User titles."""

    MR = "MR"
    MS = "MS"
    DR = "DR"
    PROF = "PROF"


class UserBase(BaseModel):
    """User base fields."""

    first_name: str
    last_name: str
    links: UserLinks
    # TODO: Either define a custom Enum and map to different db categories or
    #  switch to using Tags
    research_interests: list[ArxivCategory] = []
    title: UserTitle | None = None
    affiliation: str | None = None
    bday: datetime | None = None
    bio: str | None = None


class UserCreateInput(UserBase):
    """User registration fields."""

    email: EmailStr
    password: str


class UserUpdateInput(UserBase):
    """User update fields."""

    first_name: str | None = None
    last_name: str | None = None
    bib_links: UserLinks | None = None


class User(Document, UserBase):
    """User DB representation."""

    id: str
    email: Annotated[str, Indexed(EmailStr, unique=True)]

    @classmethod
    async def by_email(cls, email: str):
        """Get a user by email."""
        return await cls.find_one(cls.email == email)


class UserResearchInterestsView(BaseModel):
    """User research interests view."""

    research_interests: list[ArxivCategory]
