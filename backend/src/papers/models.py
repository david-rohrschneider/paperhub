from datetime import datetime
from enum import Enum
from typing import Literal

from pydantic import BaseModel, HttpUrl
from semanticscholar.Paper import Paper as SSPaper
from semanticscholar.PublicationVenue import PublicationVenue
from src.adapters.semantic_scholar_adapter import Autocomplete

from src.config import CONFIG
from src.users.models import UserFieldOfStudy


class ExternalIds(BaseModel):
    ArXiv: str | None = None
    MAG: str | None = None
    ACL: str | None = None
    PubMed: str | None = None
    Medline: str | None = None
    PubMedCentral: str | None = None
    DBLP: str | None = None
    DOI: str | None = None


class PublicationType(str, Enum):
    REVIEW = "Review"
    JOURNAL_ARTICLE = "JournalArticle"
    CASE_REPORT = "CaseReport"
    CLINICAL_TRIAL = "ClinicalTrial"
    CONFERENCE = "Conference"
    DATASET = "Dataset"
    EDITORIAL = "Editorial"
    LETTERS_AND_COMMENTS = "LettersAndComments"
    META_ANALYSIS = "MetaAnalysis"
    NEWS = "News"
    STUDY = "Study"
    BOOK = "Book"
    BOOK_SECTION = "BookSection"


class Venue(BaseModel):
    id: str
    name: str
    alternate_names: list[str] = []
    alternate_urls: list[HttpUrl] = []
    issn: str | None = None
    type: Literal["journal", "conference"] | None = None
    url: HttpUrl | None = None

    @classmethod
    def from_semantic_scholar(cls, v: PublicationVenue) -> "Venue":
        return cls(
            id=v.id,
            name=v.name,
            alternate_names=v.alternate_names or [],
            alternate_urls=v.alternate_urls or [],
            issn=v.issn,
            type=v.type,
            url=v.url,
        )


class PaperResponse(BaseModel):
    id: str
    external_ids: ExternalIds
    title: str
    published_at: datetime
    authors: list[str]
    citations: int
    publication_types: list[PublicationType] = []
    abstract: str | None = None
    likes: int = 0
    open_pdf_url: HttpUrl | None = None
    venue: Venue | None = None
    thumbnail_url: HttpUrl

    @classmethod
    def from_semantic_scholar(cls, p: SSPaper, likes: int) -> "PaperResponse":
        thumbnail_url = CONFIG.root_url + f"/papers/{p.paperId}/thumbnail"

        if not p.openAccessPdf:
            thumbnail_url += "?locked=true"

        publication_types = []
        if p.publicationTypes:
            publication_types = [PublicationType(pt) for pt in p.publicationTypes]

        return cls(
            id=p.paperId,
            external_ids=ExternalIds(**p.externalIds),
            title=p.title,
            published_at=p.publicationDate,
            authors=[a.name for a in p.authors],
            publication_types=publication_types,
            abstract=p.abstract,
            citations=p.citationCount,
            likes=likes,
            open_pdf_url=p.openAccessPdf["url"] if p.openAccessPdf else None,
            venue=(
                Venue.from_semantic_scholar(p.publicationVenue)
                if p.publicationVenue
                else None
            ),
            thumbnail_url=thumbnail_url,
        )


class PaperLeanResponse(BaseModel):
    id: str
    title: str
    published_at: datetime
    authors: list[str]
    thumbnail_url: HttpUrl

    @classmethod
    def from_semantic_scholar(cls, p: SSPaper) -> "PaperLeanResponse":
        thumbnail_url = CONFIG.root_url + f"/papers/{p.paperId}/thumbnail"

        if not p.openAccessPdf:
            thumbnail_url += "?locked=true"

        return cls(
            id=p.paperId,
            title=p.title,
            published_at=p.publicationDate,
            authors=[a.name for a in p.authors],
            thumbnail_url=thumbnail_url,
        )


class PaperAutocompleteResponse(BaseModel):
    id: str
    title: str
    authors_year: str

    @classmethod
    def from_semantic_scholar(cls, a: Autocomplete) -> "PaperAutocompleteResponse":
        return cls(
            id=a.id,
            title=a.title,
            authors_year=a.authors_year,
        )


class PaperSearchInput(BaseModel):
    query: str
    publication_types: list[PublicationType] | None = None
    open_access_pdf: bool = False
    venues: list[str] | None = None
    fields_of_study: list[UserFieldOfStudy] | None = None
    publication_date_start: datetime | None = None
    publication_date_end: datetime | None = None
    min_citation_count: int | None = None
