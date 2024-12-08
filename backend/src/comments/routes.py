from typing import Annotated
from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException, status

from src.auth.dependencies import current_user_id
from src.comments.models import Comment, CommentCreateInput, CommentUpdateInput
from src.papers.models import Paper


router = APIRouter(prefix="/comments", tags=["Comment"])


@router.post("")
async def create_comment(
    body: CommentCreateInput, uid: Annotated[str, Depends(current_user_id)]
) -> Comment:
    """Create a comment on a paper.

    Args:
        body (CommentCreateInput): Comment input.
        uid (str): Firebase user ID.

    Returns:
        Comment: Created comment.
    """
    paper_exists = await Paper.find_one(Paper.id == body.paper_id).exists()

    if not paper_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    comment = await Comment(
        user_id=uid,
        paper_id=body.paper_id,
        text=body.text,
    ).create()

    await Paper.find_one(Paper.id == body.paper_id).inc({Paper.comments: 1})

    return comment


@router.get("")
async def get_comments_for_paper(paper_id: PydanticObjectId) -> list[Comment]:
    """Get comments for a paper.

    Args:
        paper_id (PydanticObjectId): Paper ID.

    Returns:
        list[Comment]: List of comments.
    """
    # TODO: Add pagination
    return await Comment.find(Comment.paper_id == paper_id).to_list()


@router.patch("/{comment_id}")
async def update_comment(
    comment_id: PydanticObjectId,
    body: CommentUpdateInput,
    uid: Annotated[str, Depends(current_user_id)],
) -> Comment:
    """Update a comment.

    Args:
        comment_id (PydanticObjectId): Comment ID.
        body (CommentUpdateInput): Comment input.
        uid (str): Firebase user ID.

    Returns:
        Comment: Updated comment.
    """
    comment = await Comment.find_one(Comment.id == comment_id, Comment.user_id == uid)

    if comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    comment.text = body.text
    await comment.save()

    return comment


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    comment_id: PydanticObjectId, uid: Annotated[str, Depends(current_user_id)]
) -> None:
    """Delete a comment.

    Args:
        comment_id (PydanticObjectId): Comment ID.
        uid (str): Firebase user ID.
    """
    comment = await Comment.find_one(Comment.id == comment_id, Comment.user_id == uid)

    if comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    await comment.delete()

    await Paper.find_one(Paper.id == comment.paper_id).inc({Paper.comments: -1})
