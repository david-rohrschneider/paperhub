from datetime import datetime

from beanie import PydanticObjectId
from fastapi import HTTPException, status
from semanticscholar.Paper import Paper

from src.dependencies import Pagination
from src.libraries.models import (
    Library,
    LibraryCreateInput,
    LibraryPapersInput,
    LibraryUpdateInput,
)
from src.adapters import semantic_scholar_adapter as ss_adapter


async def create(body: LibraryCreateInput, uid: str) -> Library:
    library = await Library(
        user_id=uid,
        title=body.title,
        private=body.private,
        default=False,
        created_at=datetime.now(),
    ).create()

    return library


async def get_many_by_user(uid: str, pagination: Pagination) -> list[Library]:
    libraries = (
        await Library.find(Library.user_id == uid)
        .skip(pagination.offset)
        .limit(pagination.limit)
        .to_list()
    )
    # TODO: Aggregate papers count and remove papers field from response
    return libraries


async def get_one_by_user(
    library_id: PydanticObjectId, uid: str, pagination: Pagination
) -> tuple[Library, list[Paper]]:
    library = await Library.find_one(Library.id == library_id, Library.user_id == uid)

    if not library:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if len(library.papers) == 0:
        return library, []

    paper_ids = library.papers[pagination.offset : pagination.offset + pagination.limit]
    papers = await ss_adapter.find_many_by_ids(paper_ids)

    return library, papers


async def get_one_public(
    library_id: PydanticObjectId, pagination: Pagination
) -> tuple[Library, list[Paper]]:
    library = await Library.find_one(Library.id == library_id, Library.private == False)

    if not library:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if len(library.papers) == 0:
        return library, []

    paper_ids = library.papers[pagination.offset : pagination.offset + pagination.limit]
    papers = await ss_adapter.find_many_by_ids(paper_ids)

    return library, papers


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
    library = await library.save()

    return library


async def remove_papers(
    library_id: PydanticObjectId, body: LibraryPapersInput, uid: str
) -> Library:
    library = await Library.find_one(Library.id == library_id, Library.user_id == uid)

    if not library:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    library.papers = list(set(library.papers) - body.paper_ids)
    library = await library.save()

    return library


async def delete(library_id: PydanticObjectId, uid: str):
    library = await Library.find_one(Library.id == library_id, Library.user_id == uid)

    if not library:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if library.default:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    await library.delete()
