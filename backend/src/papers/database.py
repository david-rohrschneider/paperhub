from datetime import datetime, timedelta

from semanticscholar.Paper import Paper as SSPaper

from src.dependencies import Pagination
from src.likes import database as likes_db
from src.likes.models import Like, LikePaperView
from src.users import database as users_db
from src.papers.models import PaperSearchInput
from src.adapters import semantic_scholar_adapter as ss_adapter
from src.adapters.semantic_scholar_adapter import Autocomplete
from src.config import CONFIG


async def get_feed(
    uid: str, pagination: Pagination
) -> tuple[list[SSPaper], dict[str, int]]:
    likes = (
        await Like.find(Like.user_id == uid)
        .project(LikePaperView)
        .sort((Like.created_at, -1))
        .limit(CONFIG.feed.num_positive_samples)
        .to_list()
    )

    if len(likes) == 0 or pagination.offset > 0:
        user = await users_db.get_by_id(uid)

        if len(likes) > 0 and pagination.offset > 0:
            # Subtract the limit because we started with recommendations
            pagination.offset -= pagination.limit

        papers, _ = await ss_adapter.find_many(
            query="n",
            limit=pagination.limit,
            offset=pagination.offset,
            fields_of_study=user.fields or None,
            publication_date_start=datetime.now() - timedelta(days=30),
        )

    else:
        papers = await ss_adapter.get_recommendations(
            [l.paper_id for l in likes], limit=pagination.limit
        )

        if len(papers) == 0:
            user = await users_db.get_by_id(uid)
            papers, _ = await ss_adapter.find_many(
                query="n",
                limit=pagination.limit,
                fields_of_study=user.fields or None,
                publication_date_start=datetime.now() - timedelta(days=30),
            )

    like_counts = await likes_db.get_paper_like_counts([p.paperId for p in papers])

    return papers, like_counts


async def get_autocomplete(query: str) -> list[Autocomplete]:
    return await ss_adapter.get_autocomplete(query)


async def search_papers(
    body: PaperSearchInput, pagination: Pagination
) -> tuple[list[SSPaper], dict[str, int], int]:
    papers, total = await ss_adapter.find_many(
        query=body.query,
        publication_types=body.publication_types,
        open_access_pdf=body.open_access_pdf,
        venues=body.venues,
        fields_of_study=body.fields_of_study,
        publication_date_start=body.publication_date_start,
        publication_date_end=body.publication_date_end,
        min_citation_count=body.min_citation_count,
        limit=pagination.limit,
        offset=pagination.offset,
    )

    like_counts = await likes_db.get_paper_like_counts([p.paperId for p in papers])

    return papers, like_counts, total
