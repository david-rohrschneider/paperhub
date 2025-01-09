from datetime import datetime

from beanie import PydanticObjectId
from fastapi import HTTPException, status
from semanticscholar.Paper import Paper

from src.dependencies import Pagination
from src.libraries.models import (
    Library,
    LibraryCreateInput,
    LibraryLeanView,
    LibraryPapersView,
    LibraryResponse,
    LibraryPapersInput,
    LibraryUpdateInput,
)
from src.adapters import semantic_scholar_adapter as ss_adapter
from src.models import PaginatedResponse
from src.papers.models import PaperResponse
from src.papers.thumbnail import generate_thumbnails
from src.util import get_pagination_aggregation
from src.likes import database as likes_db


async def create(body: LibraryCreateInput, uid: str) -> Library:
    library = await Library(
        user_id=uid,
        title=body.title,
        private=body.private,
        default=False,
        created_at=datetime.now(),
    ).create()

    return library


async def get_many_by_user(
    uid: str, pagination: Pagination, contains_paper: str | None = None
) -> PaginatedResponse[LibraryResponse]:
    projection = {
        "_id": 1,
        "user_id": 1,
        "title": 1,
        "default": 1,
        "created_at": 1,
        "updated_at": 1,
        "private": 1,
        "papers": 1,
        "num_papers": {"$size": "$papers"},
    }

    if contains_paper is not None:
        projection["contains_paper"] = {"$in": [contains_paper, "$papers"]}

    libraries = (
        await Library.find(Library.user_id == uid)
        .sort(-Library.default, -Library.updated_at)
        .aggregate(
            get_pagination_aggregation(pagination, projection),
            projection_model=PaginatedResponse[LibraryResponse],
        )
        .to_list()
    )

    return libraries[0]


async def get_one(
    library_id: PydanticObjectId, uid: str | None = None
) -> LibraryLeanView:
    query = [Library.id == library_id]

    if uid is not None:
        query.append(Library.user_id == uid)
    else:
        query.append(Library.private == False)

    library = await Library.find_one(*query).project(LibraryLeanView)

    if not library:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return library


async def get_papers(
    library_id: PydanticObjectId, pagination: Pagination, uid: str | None = None
) -> PaginatedResponse[PaperResponse]:
    query = [Library.id == library_id]

    if uid is not None:
        query.append(Library.user_id == uid)
    else:
        query.append(Library.private == False)

    library = await Library.find_one(*query).project(LibraryPapersView)

    if not library:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if len(library.papers) == 0:
        return PaginatedResponse[PaperResponse](data=[], total=0)

    paper_ids = library.papers[pagination.offset : pagination.offset + pagination.limit]
    papers = await ss_adapter.find_many_by_ids(paper_ids)

    like_counts = await likes_db.get_paper_like_counts([p.paperId for p in papers])

    thumbnail_urls = [
        (p.openAccessPdf["url"], p.paperId) for p in papers if p.openAccessPdf
    ]
    presigned_urls = (
        await generate_thumbnails(thumbnail_urls) if len(thumbnail_urls) > 0 else {}
    )

    papers = [
        PaperResponse.from_semantic_scholar(
            p,
            like_counts[p.paperId],
            presigned_urls[p.paperId] if p.paperId in presigned_urls else None,
        )
        for p in papers
    ]

    return PaginatedResponse[PaperResponse](data=papers, total=len(library.papers))


async def update(
    library_id: PydanticObjectId, body: LibraryUpdateInput, uid: str
) -> Library:
    if body.title is None and body.private is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    library = await Library.find_one(Library.id == library_id, Library.user_id == uid)

    if not library:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if library.default:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    library = await library.set(body.model_dump(exclude_unset=True))

    return library


async def clear(library_id: PydanticObjectId, uid: str) -> Library:
    library = await Library.find_one(Library.id == library_id, Library.user_id == uid)

    if not library:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    library.papers = []
    library = await library.save()

    return library


async def add_papers(
    library_id: PydanticObjectId, body: LibraryPapersInput, uid: str
) -> Library:
    library = await Library.find_one(Library.id == library_id, Library.user_id == uid)

    if not library:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    valid_papers = await ss_adapter.find_many_by_ids(
        list(body.paper_ids), fields=["paperId"]
    )

    if len(valid_papers) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    valid_paper_ids = [paper.paperId for paper in valid_papers]
    new_papers = list(set(library.papers + valid_paper_ids))

    if len(new_papers) == len(library.papers):
        return library

    library.papers = new_papers
    library.updated_at = datetime.now()
    library = await library.save()

    return library


async def remove_papers(
    library_id: PydanticObjectId, body: LibraryPapersInput, uid: str
) -> Library:
    library = await Library.find_one(Library.id == library_id, Library.user_id == uid)

    if not library:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    library.papers = list(set(library.papers) - body.paper_ids)
    library.updated_at = datetime.now()
    library = await library.save()

    return library


async def delete(library_id: PydanticObjectId, uid: str):
    library = await Library.find_one(Library.id == library_id, Library.user_id == uid)

    if not library:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if library.default:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    await library.delete()
