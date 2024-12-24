import os
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends
from fastapi.responses import FileResponse

from src.auth.dependencies import current_user_id
from src.dependencies import Pagination
from src.papers import database as papers_db
from src.papers.models import PaperAutocompleteResponse, PaperResponse, PaperSearchInput
from src.config import CONFIG
from src.papers.thumbnail import generate_thumbnails


router = APIRouter(prefix="/papers", tags=["Paper"])


@router.get("")
async def get_feed(
    uid: Annotated[str, Depends(current_user_id)],
    pagination: Annotated[Pagination, Depends(Pagination)],
    background_tasks: BackgroundTasks,
) -> list[PaperResponse]:
    """Get a feed of papers based on user research interests.

    Args:
        uid (str): Firebase user ID.
        pagination (Pagination): Pagination parameters.
        background_tasks (BackgroundTasks): FastAPI Background tasks.

    Returns:
        list[PaperResponse]: List of papers.
    """
    papers, like_counts = await papers_db.get_feed(uid, pagination)

    thumbnail_urls = [
        (p.openAccessPdf["url"], p.paperId) for p in papers if p.openAccessPdf
    ]
    background_tasks.add_task(generate_thumbnails, thumbnail_urls)

    return [
        PaperResponse.from_semantic_scholar(paper, like_counts[paper.paperId])
        for paper in papers
    ]


@router.get("/autocomplete")
async def get_autocomplete(query: str) -> list[PaperAutocompleteResponse]:
    """Get autocomplete suggestions for a query.

    Args:
        query (str): Query.

    Returns:
        list[PaperAutocompleteResponse]: List of autocomplete suggestions.
    """
    suggestions = await papers_db.get_autocomplete(query)
    return [PaperAutocompleteResponse.from_semantic_scholar(s) for s in suggestions]


@router.post("/search")
async def search_papers(
    body: PaperSearchInput,
    pagination: Annotated[Pagination, Depends(Pagination)],
    background_tasks: BackgroundTasks,
) -> list[PaperResponse]:
    papers, like_counts = await papers_db.search_papers(body, pagination)

    thumbnail_urls = [
        (p.openAccessPdf["url"], p.paperId) for p in papers if p.openAccessPdf
    ]
    background_tasks.add_task(generate_thumbnails, thumbnail_urls)

    return [
        PaperResponse.from_semantic_scholar(paper, like_counts[paper.paperId])
        for paper in papers
    ]


@router.get("/{paper_id}/thumbnail")
async def get_thumbnail(paper_id: str, locked: bool = False) -> FileResponse:
    """Get a thumbnail by paper ID.

    Args:
        paper_id (str): Paper ID.
        locked (bool): Whether the paper is not publicly available.

    Returns:
        FileResponse: The thumbnail file.
    """
    if locked:
        path = os.path.join(
            CONFIG.thumbnail.local_folder, f"locked.{CONFIG.thumbnail.format}"
        )
        path = os.path.abspath(path)
        return FileResponse(path)

    path = os.path.join(
        CONFIG.thumbnail.local_folder, f"{paper_id}.{CONFIG.thumbnail.format}"
    )
    path = os.path.abspath(path)

    if not os.path.exists(path):
        path = os.path.join(
            CONFIG.thumbnail.local_folder, f"fallback.{CONFIG.thumbnail.format}"
        )
        path = os.path.abspath(path)

    return FileResponse(path)
