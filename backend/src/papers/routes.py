import os

from typing import Annotated
from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from beanie.operators import In
from fastapi.responses import FileResponse

from src.auth.dependencies import current_user_id
from src.papers.models import Paper, PaperIdView, PaperResponse, PaperSource
from src.papers.adapters import arxiv_adapter
from src.config import CONFIG
from src.papers.thumbnail import (
    generate_thumbnail_from_url,
    generate_thumbnails_from_urls,
)
from src.users.models import User, UserResearchInterestsView


router = APIRouter(prefix="/papers", tags=["Paper"])


@router.get("")
async def get_paper_feed(
    uid: Annotated[str, Depends(current_user_id)],
) -> list[PaperResponse]:
    """Get a feed of papers based on user research interests.

    Args:
        uid (str): Firebase user ID.

    Returns:
        list[PaperResponse]: List of papers.
    """
    user = await User.find_one(User.id == uid).project(UserResearchInterestsView)
    res = arxiv_adapter.find_by_categories(user.research_interests)

    res_ids = [arxiv_adapter.get_plain_id(r) for r in res]
    existing_papers = await Paper.find(In(Paper.source_id, res_ids)).to_list()
    existing_ids = {p.source_id for p in existing_papers}

    new_res = [r for r in res if arxiv_adapter.get_plain_id(r) not in existing_ids]
    ret_papers = existing_papers

    if len(new_res) > 0:
        new_papers = [Paper.from_arxiv(r) for r in new_res]
        await Paper.insert_many(new_papers)
        generate_thumbnails_from_urls(
            [r.pdf_url for r in new_res], [str(p.id) for p in new_papers]
        )
        ret_papers += new_papers

    return [
        PaperResponse(
            **paper.model_dump(),
            source_url=CONFIG.arxiv.source_url_base + paper.source_id,
            thumbnail_url=CONFIG.root_url + f"/papers/{paper.id}/thumbnail",
        )
        for paper in ret_papers
    ]


@router.get("/{paper_id}/thumbnail")
async def get_thumbnail(paper_id: str) -> FileResponse:
    """Get a thumbnail by paper ID.

    Args:
        paper_id (str): Paper ID.

    Returns:
        FileResponse: The thumbnail file.
    """
    path = os.path.join(
        CONFIG.thumbnail.local_folder, f"{paper_id}.{CONFIG.thumbnail.format}"
    )
    path = os.path.abspath(path)

    if not os.path.exists(path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return FileResponse(path)


@router.get("/{paper_id}")
async def get_paper_by_id(
    paper_id: PydanticObjectId,
) -> PaperResponse:
    """Get a paper by ID.

    Args:
        paper_id (PydanticObjectId): Paper ID.

    Returns:
        PaperResponse: The paper.

    Raises:
        HTTPException: If the paper is not found.
    """
    paper = await Paper.get(paper_id)

    if paper is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    source_url = CONFIG.arxiv.source_url_base + paper.source_id
    thumbnail_url = CONFIG.root_url + f"/papers/{paper.id}/thumbnail"
    return PaperResponse(
        **paper.model_dump(),
        source_url=source_url,
        thumbnail_url=thumbnail_url,
    )


@router.get("/{paper_source}/{paper_source_id}")
async def get_paper_by_source_id(
    paper_source: PaperSource,
    paper_source_id: str,
) -> PaperResponse:
    """Get a paper by source and source ID.

    Args:
        paper_source (PaperSource): Paper source.
        paper_source_id (str): Paper source ID.

    Returns:
        PaperResponse: The paper.
    """
    plain_id = arxiv_adapter.get_plain_id(paper_source_id)
    paper = await Paper.find_one(Paper.source_id == plain_id)

    if paper is not None:
        source_url = CONFIG.arxiv.source_url_base + plain_id
        thumbnail_url = CONFIG.root_url + f"/papers/{paper.id}/thumbnail"
        return PaperResponse(
            **paper.model_dump(),
            source_url=source_url,
            thumbnail_url=thumbnail_url,
        )

    if paper_source == PaperSource.ARXIV:
        res = arxiv_adapter.find_by_id(plain_id)
        paper = await Paper.from_arxiv(res).create()

        generate_thumbnail_from_url(
            res.pdf_url,
            str(paper.id),
        )

        source_url = CONFIG.arxiv.source_url_base + paper_source_id
        thumbnail_url = CONFIG.root_url + f"/papers/{paper.id}/thumbnail"
        return PaperResponse(
            **paper.model_dump(),
            source_url=source_url,
            thumbnail_url=thumbnail_url,
        )

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
