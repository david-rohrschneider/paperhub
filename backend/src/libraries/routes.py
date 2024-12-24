from typing import Annotated

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, status

from src.auth.dependencies import current_user_id
from src.dependencies import Pagination
from src.libraries.models import (
    Library,
    LibraryPapersInput,
    LibraryCreateInput,
    LibraryResponse,
    LibraryUpdateInput,
)
from src.libraries import database as libraries_db
from src.papers.models import PaperLeanResponse


router = APIRouter(prefix="/libraries", tags=["Library"])


@router.post("")
async def create_library(
    body: LibraryCreateInput,
    uid: Annotated[str, Depends(current_user_id)],
) -> Library:
    """Create a new library.

    Args:
        body (LibraryCreateInput): The library data.
        uid (str): The user ID.

    Returns:
        Library: The created library.
    """
    return await libraries_db.create(body, uid)


@router.get("")
async def get_libraries(
    pagination: Annotated[Pagination, Depends(Pagination)],
    uid: Annotated[str, Depends(current_user_id)],
) -> list[Library]:
    """Get all libraries of the user.

    Args:
        pagination (Pagination): Pagination parameters.
        uid (str): The user ID.

    Returns:
        list[Library]: The libraries.
    """
    return await libraries_db.get_many_by_user(uid, pagination)


@router.get("/{library_id}")
async def get_library(
    library_id: PydanticObjectId,
    pagination: Annotated[Pagination, Depends(Pagination)],
    uid: Annotated[str, Depends(current_user_id)],
) -> LibraryResponse:
    """Get a library by ID.

    Args:
        library_id (PydanticObjectId): The library ID.
        pagination (Pagination): Pagination parameters for papers in libray.
        uid (str): The user ID.

    Returns:
        LibraryResponse: The library.

    Raises:
        HTTPException: If the library is not found.
    """
    library, papers = await libraries_db.get_one_by_user(library_id, uid, pagination)
    papers = [PaperLeanResponse.from_semantic_scholar(p) for p in papers]

    return LibraryResponse(**library.model_dump(exclude=("papers")), papers=papers)


@router.get("/public/{library_id}")
async def get_public_library(
    library_id: PydanticObjectId, pagination: Annotated[Pagination, Depends(Pagination)]
) -> LibraryResponse:
    """Get a public library by ID.

    Args:
        library_id (PydanticObjectId): The library ID.
        pagination (Pagination): Pagination parameters for papers in libray.

    Returns:
        LibraryResponse: The library.

    Raises:
        HTTPException: If the library is not found.
    """
    library, papers = await libraries_db.get_one_public(library_id, pagination)
    papers = [PaperLeanResponse.from_semantic_scholar(p) for p in papers]

    return LibraryResponse(**library.model_dump(exclude=("papers")), papers=papers)


@router.patch("/{library_id}")
async def update_library(
    library_id: PydanticObjectId,
    body: LibraryUpdateInput,
    uid: Annotated[str, Depends(current_user_id)],
) -> Library:
    """Update a library.

    Args:
        library_id (PydanticObjectId): The library ID.
        body (LibraryUpdateInput): The library data.
        uid (str): The user ID.

    Returns:
        Library: The updated library.

    Raises:
        HTTPException: If the library is not found or the request is invalid.
    """
    return await libraries_db.update(library_id, body, uid)


@router.patch("/{library_id}/clear")
async def clear_library(
    library_id: PydanticObjectId, uid: Annotated[str, Depends(current_user_id)]
) -> Library:
    """Clear a library.

    Args:
        library_id (PydanticObjectId): The library ID.
        uid (str): The user ID.

    Returns:
        Library: The cleared library.

    Raises:
        HTTPException: If the library is not found.
    """
    return await libraries_db.clear(library_id, uid)


@router.post("/{library_id}")
async def add_papers_to_library(
    library_id: PydanticObjectId,
    body: LibraryPapersInput,
    uid: Annotated[str, Depends(current_user_id)],
) -> Library:
    """Add (multiple) papers to a library.

    Args:
        library_id (PydanticObjectId): The library ID.
        body (LibraryPapersInput): Request body containing the paper IDs.
        uid (str): The user ID.

    Returns:
        Library: The updated library.

    Raises:
        HTTPException: If the library is not found or the request is invalid.
    """
    return await libraries_db.add_papers(library_id, body, uid)


@router.patch("/{library_id}/remove-papers")
async def remove_papers_from_library(
    library_id: PydanticObjectId,
    body: LibraryPapersInput,
    uid: Annotated[str, Depends(current_user_id)],
) -> Library:
    """Remove (multiple) papers from a library.

    Args:
        library_id (PydanticObjectId): The library ID.
        body (LibraryPapersInput): Request body containing the paper IDs.
        uid (str): The user ID.

    Returns:
        Library: The updated library.

    Raises:
        HTTPException: If the library is not found.
    """
    return await libraries_db.remove_papers(library_id, body, uid)


@router.delete("/{library_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_library(
    library_id: PydanticObjectId, uid: Annotated[str, Depends(current_user_id)]
) -> None:
    """Delete a library.

    Args:
        library_id (PydanticObjectId): The library ID.
        uid (str): The user ID.

    Raises:
        HTTPException: If the library is not found or is the default library.
    """
    await libraries_db.delete(library_id, uid)
