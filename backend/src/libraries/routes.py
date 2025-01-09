from typing import Annotated

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, status

from src.auth.dependencies import current_user_id
from src.dependencies import Pagination
from src.libraries.models import (
    LibraryResponse,
    LibraryPapersInput,
    LibraryCreateInput,
    LibraryResponse,
    LibraryUpdateInput,
)
from src.libraries import database as libraries_db
from src.models import PaginatedResponse
from src.papers.models import PaperResponse


router = APIRouter(prefix="/libraries", tags=["Library"])


@router.post("")
async def create_library(
    body: LibraryCreateInput,
    uid: Annotated[str, Depends(current_user_id)],
) -> LibraryResponse:
    """Create a new library.

    Args:
        body (LibraryCreateInput): The library data.
        uid (str): The user ID.

    Returns:
        LibraryResponse: The created library.
    """
    library = await libraries_db.create(body, uid)
    return LibraryResponse(**library.model_dump(), num_papers=0)


@router.get("")
async def get_libraries(
    pagination: Annotated[Pagination, Depends(Pagination)],
    uid: Annotated[str, Depends(current_user_id)],
    contains_paper: str | None = None,
) -> PaginatedResponse[LibraryResponse]:
    """Get all libraries of the user.

    Args:
        pagination (Pagination): Pagination parameters.
        uid (str): The user ID.
        contains_paper (str | None): The paper ID to check if it is in the library.

    Returns:
        PaginatedResponse[LibraryResponse]: The libraries with paper counts and optional contains_paper field.
    """
    return await libraries_db.get_many_by_user(uid, pagination, contains_paper)


@router.get("/{library_id}")
async def get_library(
    library_id: PydanticObjectId,
    uid: Annotated[str, Depends(current_user_id)],
) -> LibraryResponse:
    """Get a library by ID.

    Args:
        library_id (PydanticObjectId): The library ID.
        uid (str): The user ID.

    Returns:
        LibraryResponse: The library.

    Raises:
        HTTPException: If the library is not found.
    """
    library = await libraries_db.get_one(library_id, uid)
    return LibraryResponse(**library.model_dump())


@router.get("/{library_id}/papers")
async def get_library_papers(
    library_id: PydanticObjectId,
    pagination: Annotated[Pagination, Depends(Pagination)],
    uid: Annotated[str, Depends(current_user_id)],
) -> PaginatedResponse[PaperResponse]:
    """Get all papers in a library.

    Args:
        library_id (PydanticObjectId): The library ID.
        pagination (Pagination): Pagination parameters.
        uid (str): The user ID.

    Returns:
        PaginatedResponse[PaperResponse]: The papers in the library.
    """
    return await libraries_db.get_papers(library_id, pagination, uid)


@router.get("/public/{library_id}")
async def get_public_library(library_id: PydanticObjectId) -> LibraryResponse:
    """Get a public library by ID.

    Args:
        library_id (PydanticObjectId): The library ID.

    Returns:
        LibraryResponse: The library.

    Raises:
        HTTPException: If the library is not found.
    """
    library = await libraries_db.get_one(library_id)
    return LibraryResponse(**library.model_dump())


@router.get("/public/{library_id}/papers")
async def get_public_library_papers(
    library_id: PydanticObjectId,
    pagination: Annotated[Pagination, Depends(Pagination)],
) -> PaginatedResponse[PaperResponse]:
    """Get all papers in a library.

    Args:
        library_id (PydanticObjectId): The library ID.
        pagination (Pagination): Pagination parameters.

    Returns:
        PaginatedResponse[PaperResponse]: The papers in the library.
    """
    return await libraries_db.get_papers(library_id, pagination)


@router.patch("/{library_id}")
async def update_library(
    library_id: PydanticObjectId,
    body: LibraryUpdateInput,
    uid: Annotated[str, Depends(current_user_id)],
) -> LibraryResponse:
    """Update a library.

    Args:
        library_id (PydanticObjectId): The library ID.
        body (LibraryUpdateInput): The library data.
        uid (str): The user ID.

    Returns:
        LibraryResponse: The updated library.

    Raises:
        HTTPException: If the library is not found or the request is invalid.
    """
    library = await libraries_db.update(library_id, body, uid)
    return LibraryResponse(**library.model_dump(), num_papers=len(library.papers))


@router.patch("/{library_id}/clear")
async def clear_library(
    library_id: PydanticObjectId, uid: Annotated[str, Depends(current_user_id)]
) -> LibraryResponse:
    """Clear a library.

    Args:
        library_id (PydanticObjectId): The library ID.
        uid (str): The user ID.

    Returns:
        LibraryResponse: The cleared library.

    Raises:
        HTTPException: If the library is not found.
    """
    library = await libraries_db.clear(library_id, uid)
    return LibraryResponse(**library.model_dump(), num_papers=0)


@router.post("/{library_id}")
async def add_papers_to_library(
    library_id: PydanticObjectId,
    body: LibraryPapersInput,
    uid: Annotated[str, Depends(current_user_id)],
) -> LibraryResponse:
    """Add (multiple) papers to a library.

    Args:
        library_id (PydanticObjectId): The library ID.
        body (LibraryPapersInput): Request body containing the paper IDs.
        uid (str): The user ID.

    Returns:
        LibraryResponse: The updated library.

    Raises:
        HTTPException: If the library is not found or the request is invalid.
    """
    library = await libraries_db.add_papers(library_id, body, uid)
    return LibraryResponse(**library.model_dump(), num_papers=len(library.papers))


@router.patch("/{library_id}/remove-papers")
async def remove_papers_from_library(
    library_id: PydanticObjectId,
    body: LibraryPapersInput,
    uid: Annotated[str, Depends(current_user_id)],
) -> LibraryResponse:
    """Remove (multiple) papers from a library.

    Args:
        library_id (PydanticObjectId): The library ID.
        body (LibraryPapersInput): Request body containing the paper IDs.
        uid (str): The user ID.

    Returns:
        LibraryResponse: The updated library.

    Raises:
        HTTPException: If the library is not found.
    """
    library = await libraries_db.remove_papers(library_id, body, uid)
    return LibraryResponse(**library.model_dump(), num_papers=len(library.papers))


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
