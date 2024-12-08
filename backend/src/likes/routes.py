from typing import Annotated
from beanie import PydanticObjectId
from beanie.operators import In
from fastapi import APIRouter, Depends, HTTPException, status
from pymongo.errors import DuplicateKeyError

from src.auth.dependencies import current_user_id
from src.likes.models import Like, LikesWithPapersResponse, LikesWithUsersResponse
from src.papers.models import Paper, PaperBasicInfoView
from src.users.models import User, UserBasicInfoView


router = APIRouter(prefix="/likes", tags=["Like"])


@router.post("/paper/{paper_id}", status_code=status.HTTP_201_CREATED)
async def create_like(
    paper_id: PydanticObjectId, uid: Annotated[str, Depends(current_user_id)]
) -> None:
    """Create a like for a paper.

    Args:
        paper_id (PydanticObjectId): Paper ID.
        uid (str): Firebase user ID.
    """
    paper_exists = await Paper.find_one(Paper.id == paper_id).exists()

    if not paper_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    try:
        await Like(paper_id=paper_id, user_id=uid).create()
    except DuplicateKeyError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    await Paper.find_one(Paper.id == paper_id).inc({Paper.likes: 1})


@router.get("/paper/{paper_id}")
async def get_likes_for_paper(paper_id: PydanticObjectId) -> LikesWithUsersResponse:
    """Get likes for a paper.

    Args:
        paper_id (PydanticObjectId): Paper ID.

    Returns:
        LikesWithUsersResponse: Likes response with users.
    """
    # TODO: Add pagination
    likes = await Like.find(Like.paper_id == paper_id).to_list()
    total_likes = await Like.find(Like.paper_id == paper_id).count()

    if total_likes == 0:
        return LikesWithUsersResponse(total_likes=0, users=[])

    users = (
        await User.find(In(User.id, [l.user_id for l in likes]))
        .project(UserBasicInfoView)
        .to_list()
    )

    return LikesWithUsersResponse(total_likes=total_likes, users=users)


@router.get("")
async def get_user_likes(
    uid: Annotated[str, Depends(current_user_id)]
) -> LikesWithPapersResponse:
    """Get likes for a user.

    Args:
        uid (str): Firebase user ID.

    Returns:
        LikesWithPapersResponse: Likes response with papers.
    """
    # TODO: Add pagination
    total_likes = await Like.find(Like.user_id == uid).count()

    if total_likes == 0:
        return LikesWithPapersResponse(total_likes=0, papers=[])

    likes = await Like.find(Like.user_id == uid).to_list()
    papers = (
        await Paper.find(In(Paper.id, [l.paper_id for l in likes]))
        .project(PaperBasicInfoView)
        .to_list()
    )

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
    like = await Like.find_one(Like.id == like_id, Like.user_id == uid)

    if like is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    await like.delete()
    await Paper.find_one(Paper.id == like.paper_id).inc({Paper.likes: -1})
