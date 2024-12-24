from datetime import datetime
from typing import Annotated
from enum import Enum

from beanie import Document, Indexed
from pydantic import BaseModel, EmailStr, Field, HttpUrl


class UserRefs(BaseModel):
    """User social and academic links."""

    orcid: str | None = None
    google_scholar: HttpUrl | None = None
    researchgate: HttpUrl | None = None
    linkedin: HttpUrl | None = None


class UserFieldOfStudy(str, Enum):
    """User field of study."""

    CS = "CS"  # Computer Science
    MD = "MD"  # Medicine
    CH = "CH"  # Chemistry
    BI = "BI"  # Biology
    MS = "MS"  # Material Science
    PH = "PH"  # Physics
    GE = "GE"  # Geology
    PS = "PS"  # Psychology
    AR = "AR"  # Art
    HI = "HI"  # History
    GG = "GG"  # Geography
    SO = "SO"  # Sociology
    BU = "BU"  # Business
    PO = "PO"  # Political Science
    EC = "EC"  # Economics
    PL = "PL"  # Philosophy
    MA = "MA"  # Mathematics
    EN = "EN"  # Engineering
    ES = "ES"  # Environmental Science
    AF = "AF"  # Agriculture and Food
    ED = "ED"  # Education
    LA = "LA"  # Law
    LI = "LI"  # Linguistics


class UserTitle(str, Enum):
    """User titles."""

    B_SC = "B_SC"
    M_SC = "M_SC"
    DR = "DR"
    PROF = "PROF"
    PROF_DR = "PROF_DR"


class UserBase(BaseModel):
    """User base fields."""

    first_name: str
    last_name: str
    refs: UserRefs
    fields: list[UserFieldOfStudy] = []
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
    fields: list[UserFieldOfStudy] = None


class User(Document, UserBase):
    """User DB representation."""

    id: str
    email: Annotated[str, Indexed(EmailStr, unique=True)]

    @classmethod
    async def by_email(cls, email: str):
        """Get a user by email."""
        return await cls.find_one(cls.email == email)


class UserLeanView(BaseModel):
    """User basic info view."""

    id: str = Field(alias="_id")
    first_name: str
    last_name: str
    title: UserTitle | None
    affiliation: str | None
