from beanie import PydanticObjectId
from fastapi import HTTPException, status
from beanie.operators import In
from pymongo.errors import DuplicateKeyError

from src.dependencies import Pagination
from src.likes.models import Like
from src.adapters import semantic_scholar_adapter as ss_adapter
from src.models import PaginatedResponse
from src.papers.models import PaperResponse
from src.papers.thumbnail import generate_thumbnails
from src.users.models import User, UserLeanView
from src.util import get_pagination_aggregation


async def create(paper_id: str, uid: str):
    paper_exists = await ss_adapter.exists(paper_id)

    if not paper_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    try:
        await Like(paper_id=paper_id, user_id=uid).create()
    except DuplicateKeyError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)


async def get_likes_for_paper(
    paper_id: str, pagination: Pagination
) -> tuple[int, list[UserLeanView]]:
    likes = (
        await Like.find(Like.paper_id == paper_id)
        .aggregate(
            get_pagination_aggregation(pagination),
            projection_model=PaginatedResponse[Like],
        )
        .to_list()
    )

    likes, total_likes = likes[0].data, likes[0].total

    if total_likes == 0:
        return total_likes, []

    users = (
        await User.find(In(User.id, [l.user_id for l in likes]))
        .project(UserLeanView)
        .to_list()
    )

    return total_likes, users


async def get_likes_for_user(
    uid: str, pagination: Pagination
) -> tuple[int, list[PaperResponse]]:
    likes = (
        await Like.find(Like.user_id == uid)
        .aggregate(
            get_pagination_aggregation(pagination),
            projection_model=PaginatedResponse[Like],
        )
        .to_list()
    )

    likes, total_likes = likes[0].data, likes[0].total

    if total_likes == 0:
        return total_likes, []

    papers = await ss_adapter.find_many_by_ids([l.paper_id for l in likes])

    thumbnail_urls = [
        (p.openAccessPdf["url"], p.paperId) for p in papers if p.openAccessPdf
    ]
    presigned_urls = await generate_thumbnails(thumbnail_urls)

    like_counts = await get_paper_like_counts([p.paperId for p in papers])

    papers = [
        PaperResponse.from_semantic_scholar(
            p,
            like_counts[p.paperId],
            presigned_urls[p.paperId] if p.paperId in presigned_urls else None,
        )
        for p in papers
    ]

    return total_likes, papers


async def get_paper_like_counts(paper_ids: list[str]) -> dict[str, int]:
    """Get the number of likes for each paper.

    Args:
        paper_ids (list[str]): List of paper IDs.

    Returns:
        dict[str, int]: Dictionary of paper IDs and like counts.
    """
    like_counts = (
        await Like.find(In(Like.paper_id, paper_ids))
        .aggregate(
            [
                # Group by paper_id and count the number of likes
                {"$group": {"_id": "$paper_id", "count": {"$sum": 1}}},
                # Project the paper_id and count
                {"$project": {"_id": 0, "paper_id": "$_id", "count": 1}},
            ]
        )
        .to_list()
    )

    # Convert the list of like counts to a dictionary
    like_counts = {lc["paper_id"]: lc["count"] for lc in like_counts}

    # Fill in the missing paper_ids with 0 likes
    like_counts = {**{p_id: 0 for p_id in paper_ids}, **like_counts}

    return like_counts


async def delete(like_id: PydanticObjectId, uid: str):
    result = await Like.find_one(Like.id == like_id, Like.user_id == uid).delete()

    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


async def delete_by_paper_id(paper_id: str, uid: str):
    result = await Like.find_one(
        Like.paper_id == paper_id, Like.user_id == uid
    ).delete()

    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
