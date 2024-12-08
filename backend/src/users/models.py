from datetime import datetime
from typing import Annotated
from enum import Enum

from beanie import Document, Indexed
from pydantic import BaseModel, EmailStr, Field, HttpUrl

from src.papers.adapters.arxiv_adapter import ArxivCategory


class UserRefs(BaseModel):
    """User social and academic links."""

    orcid: str | None = None
    google_scholar: HttpUrl | None = None
    researchgate: HttpUrl | None = None
    linkedin: HttpUrl | None = None


class UserTitle(str, Enum):
    """User titles."""

    B_SC = "B_SC"
    M_SC = "M_SC"
    DR = "DR"
    PROF = "PROF"


class UserBase(BaseModel):
    """User base fields."""

    first_name: str
    last_name: str
    refs: UserRefs
    # TODO: Either define a custom Enum and map to different db categories or
    #  switch to using Tags
    research_interests: list[ArxivCategory] = []
    title: UserTitle | None = None
    affiliation: str | None = None
    bday: datetime | None = None
    bio: str | None = None


class UserCreateInput(UserBase):
    """User registration fields."""

    pass


class UserUpdateInput(UserBase):
    """User update fields."""

    first_name: str = None
    last_name: str = None
    refs: UserRefs = None
    research_interests: list[ArxivCategory] = None


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


class UserBasicInfoView(BaseModel):
    """User basic info view."""

    id: str = Field(alias="_id")
    first_name: str
    last_name: str
    title: UserTitle | None
    affiliation: str | None
