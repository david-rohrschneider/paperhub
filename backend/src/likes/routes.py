from typing import Annotated
from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, status

from src.auth.dependencies import current_user_id
from src.dependencies import Pagination
from src.likes import database as likes_db
from src.likes.models import LikesWithPapersResponse, LikesWithUsersResponse


router = APIRouter(prefix="/likes", tags=["Like"])


@router.post("/{paper_id}", status_code=status.HTTP_201_CREATED)
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
) -> LikesWithUsersResponse:
    """Get likes for a paper.

    Args:
        paper_id (str): Paper ID.
        pagination (Pagination): Pagination parameters.

    Returns:
        LikesWithUsersResponse: Likes response with users.
    """
    total_likes, users = await likes_db.get_likes_for_paper(paper_id, pagination)
    return LikesWithUsersResponse(total_likes=total_likes, users=users)


@router.get("")
async def get_likes_for_user(
    pagination: Annotated[Pagination, Depends(Pagination)],
    uid: Annotated[str, Depends(current_user_id)],
) -> LikesWithPapersResponse:
    """Get likes for a user.

    Args:
        pagination (Pagination): Pagination parameters.
        uid (str): Firebase user ID.

    Returns:
        LikesWithPapersResponse: Likes response with papers.
    """
    total_likes, papers = await likes_db.get_likes_for_user(uid, pagination)
    return LikesWithPapersResponse(total_likes=total_likes, papers=papers)


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
