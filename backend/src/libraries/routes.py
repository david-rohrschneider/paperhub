from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from src.auth.dependencies import current_user_id
from src.libraries.models import (
    Library,
    LibraryAddPaperInput,
    LibraryCreateInput,
    LibraryUpdateInput,
)


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
    library = await Library(
        user_id=uid,
        title=body.title,
        default=False,
        created_at=datetime.now(),
    ).create()

    return library


@router.get("")
async def get_libraries(
    uid: Annotated[str, Depends(current_user_id)],
) -> list[Library]:
    """Get all libraries of the user.

    Args:
        uid (str): The user ID.

    Returns:
        list[Library]: The libraries.
    """
    libraries = await Library.find(Library.user_id == uid).to_list()
    return libraries


@router.get("/{library_id}")
async def get_library(
    library_id: str, uid: Annotated[str, Depends(current_user_id)]
) -> Library:
    """Get a library by ID.

    Args:
        library_id (str): The library ID.
        uid (str): The user ID.

    Returns:
        Library: The library.

    Raises:
        HTTPException: If the library is not found.
    """
    library = await Library.find_one(Library.id == library_id, Library.user_id == uid)

    if not library:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return library


@router.patch("/{library_id}")
async def update_library(
    library_id: str,
    body: LibraryUpdateInput,
    uid: Annotated[str, Depends(current_user_id)],
) -> Library:
    """Update a library.

    Args:
        library_id (str): The library ID.
        body (LibraryUpdateInput): The library data.
        uid (str): The user ID.

    Returns:
        Library: The updated library.

    Raises:
        HTTPException: If the library is not found or the request is invalid.
    """
    if body.title is None and body.private is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    library = await Library.find_one(Library.id == library_id, Library.user_id == uid)

    if not library:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    library = await library.set(body.model_dump(exclude_unset=True))

    return library


@router.patch("/{library_id}/clear")
async def clear_library(
    library_id: str, uid: Annotated[str, Depends(current_user_id)]
) -> Library:
    """Clear a library.

    Args:
        library_id (str): The library ID.
        uid (str): The user ID.

    Returns:
        Library: The cleared library.

    Raises:
        HTTPException: If the library is not found.
    """
    library = await Library.find_one(Library.id == library_id, Library.user_id == uid)

    if not library:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    library.papers = []
    library = await library.save()

    return library


@router.post("/{library_id}")
async def add_paper_to_library(
    library_id: str,
    body: LibraryAddPaperInput,
    uid: Annotated[str, Depends(current_user_id)],
) -> Library:
    """Add a paper to a library.

    Args:
        library_id (str): The library ID.
        body (LibraryAddPaperInput): The paper data.
        uid (str): The user ID.

    Returns:
        Library: The updated library.

    Raises:
        HTTPException: If the library is not found or the request is invalid.
    """
    library = await Library.find_one(Library.id == library_id, Library.user_id == uid)

    if not library:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    # TODO: Implement paper verification
    # verify_paper(body.paper_id, body.paper_source)

    library.papers.append(body.paper_id)
    library = await library.save()

    return library


@router.delete("/{library_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_library(
    library_id: str, uid: Annotated[str, Depends(current_user_id)]
) -> None:
    """Delete a library.

    Args:
        library_id (str): The
        uid (str): The user ID.

    Raises:
        HTTPException: If the library is not found or is the default library.
    """
    library = await Library.find_one(Library.id == library_id, Library.user_id == uid)

    if not library:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if library.default:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    await library.delete()
