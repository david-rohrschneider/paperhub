from typing import Annotated
from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, status

from src.auth.dependencies import current_user_id
from src.dependencies import Pagination
from src.likes import database as likes_db
from src.models import PaginatedResponse
from src.papers.models import PaperResponse
from src.users.models import UserLeanView


router = APIRouter(prefix="/likes", tags=["Like"])


@router.post("/paper/{paper_id}", status_code=status.HTTP_201_CREATED)
async def create_like(
    paper_id: str, uid: Annotated[str, Depends(current_user_id)]
) -> None:
    """Create a like for a paper.

    Args:
        paper_id (str): Paper ID.
        uid (str): Firebase user ID.
    """
    await likes_db.create(paper_id, uid)


@router.get("/paper/{paper_id}")
async def get_likes_for_paper(
    paper_id: str, pagination: Annotated[Pagination, Depends(Pagination)]
) -> PaginatedResponse[UserLeanView]:
    """Get likes for a paper.

    Args:
        paper_id (str): Paper ID.
        pagination (Pagination): Pagination parameters.

    Returns:
        PaginatedResponse[UserLeanView]: Paginated response with users.
    """
    total, users = await likes_db.get_likes_for_paper(paper_id, pagination)
    return PaginatedResponse[UserLeanView](total=total, data=users)


@router.get("")
async def get_likes_for_user(
    pagination: Annotated[Pagination, Depends(Pagination)],
    uid: Annotated[str, Depends(current_user_id)],
) -> PaginatedResponse[PaperResponse]:
    """Get likes for a user.

    Args:
        pagination (Pagination): Pagination parameters.
        uid (str): Firebase user ID.

    Returns:
        PaginatedResponse[PaperResponse]: Paginated response with papers.
    """
    total, papers = await likes_db.get_likes_for_user(uid, pagination)
    return PaginatedResponse[PaperResponse](total=total, data=papers)


@router.delete("/{like_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_like(
    like_id: PydanticObjectId, uid: Annotated[str, Depends(current_user_id)]
) -> None:
    """Delete a like.

    Args:
        like_id (PydanticObjectId): Like ID.
        uid (str): Firebase user ID.
    """
    await likes_db.delete(like_id, uid)


@router.delete("/paper/{paper_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_like_for_paper(
    paper_id: str, uid: Annotated[str, Depends(current_user_id)]
) -> None:
    """Delete a like by paper id.

    Args:
        paper_id (str): Paper ID.
        uid (str): Firebase user ID.
    """
    await likes_db.delete_by_paper_id(paper_id, uid)
