from typing import Annotated

from fastapi import APIRouter, Depends

from src.auth.dependencies import current_user_id
from src.dependencies import Pagination
from src.models import PaginatedResponse
from src.papers import database as papers_db
from src.papers.models import PaperAutocompleteResponse, PaperResponse, PaperSearchInput
from src.papers.thumbnail import generate_thumbnails


router = APIRouter(prefix="/papers", tags=["Paper"])


@router.get("")
async def get_feed(
    uid: Annotated[str, Depends(current_user_id)],
    pagination: Annotated[Pagination, Depends(Pagination)],
) -> list[PaperResponse]:
    """Get a feed of papers based on user research interests.

    Args:
        uid (str): Firebase user ID.
        pagination (Pagination): Pagination parameters.

    Returns:
        list[PaperResponse]: List of papers.
    """
    papers, like_counts = await papers_db.get_feed(uid, pagination)

    thumbnail_urls = [
        (p.openAccessPdf["url"], p.paperId) for p in papers if p.openAccessPdf
    ]
    presigned_urls = await generate_thumbnails(thumbnail_urls)

    return [
        PaperResponse.from_semantic_scholar(
            paper,
            like_counts[paper.paperId],
            presigned_urls[paper.paperId] if paper.paperId in presigned_urls else None,
        )
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
) -> PaginatedResponse[PaperResponse]:
    """Search for papers.

    Args:
        body (PaperSearchInput): Search input.
        pagination (Pagination): Pagination parameters.

    Returns:
        PaginatedResponse[PaperResponse]: List of papers and total count.
    """
    papers, like_counts, total = await papers_db.search_papers(body, pagination)

    thumbnail_urls = [
        (p.openAccessPdf["url"], p.paperId) for p in papers if p.openAccessPdf
    ]
    presigned_urls = await generate_thumbnails(thumbnail_urls)

    papers = [
        PaperResponse.from_semantic_scholar(
            paper,
            like_counts[paper.paperId],
            presigned_urls[paper.paperId] if paper.paperId in presigned_urls else None,
        )
        for paper in papers
    ]

    return PaginatedResponse[PaperResponse](data=papers, total=total)
