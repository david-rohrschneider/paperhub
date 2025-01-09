from datetime import datetime

from semanticscholar import AsyncSemanticScholar
from semanticscholar.Paper import Paper
from semanticscholar.PaginatedResults import PaginatedResults
from semanticscholar.SemanticScholarException import ObjectNotFoundException
from semanticscholar.SemanticScholarObject import SemanticScholarObject

from src.users.models import UserFieldOfStudy


class Autocomplete(SemanticScholarObject):
    def __init__(self, data: dict) -> None:
        super().__init__()
        self._id = None
        self._title = None
        self._authors_year = None
        self._init_attributes(data)

    def _init_attributes(self, data: dict) -> None:
        self._data = data

        if "id" in data:
            self._id = data["id"]

        if "title" in data:
            self._title = data["title"]

        if "authorsYear" in data:
            self._authors_year = data["authorsYear"]

    @property
    def id(self) -> str:
        return self._id

    @property
    def title(self) -> str:
        return self._title

    @property
    def authors_year(self) -> str:
        return self._authors_year


class CustomAsyncSemanticScholar(AsyncSemanticScholar):
    async def get_autocomplete(self, query: str) -> list[Autocomplete]:
        """Get autocomplete suggestions for a query.

        :calls: `GET /graph/v1/paper/autocomplete?query={query} \
            <https://api.semanticscholar.org/api-docs/graph#tag/Paper-Data/operation/get_graph_get_paper_autocomplete>`

        :param str query: query to get autocomplete suggestions for.

        :returns: list of autocomplete suggestions.
        :rtype: :class:`List` of :class:`semanticscholar.Autocomplete.Autocomplete`
        """
        base_url = self.api_url + self.BASE_PATH_GRAPH
        url = f"{base_url}/paper/autocomplete"

        parameters = f"query={query}"

        data = await self._requester.get_data_async(url, parameters, self.auth_header)

        if not data or "matches" not in data:
            return []

        return [Autocomplete(suggestion) for suggestion in data["matches"]]


SCHOLAR = CustomAsyncSemanticScholar()


async def get_recommendations(ids: list[str], limit: int) -> list[Paper]:
    """Get recommendations for a list of IDs.

    Args:
        dois (list[str]): List of IDs.
        limit (int): Limit of recommendations.

    Returns:
        list[Paper]: List of recommended papers.
    """
    papers = await SCHOLAR.get_recommended_papers_from_lists(ids, limit=limit)
    return [__sanitize_paper(paper) for paper in papers]


async def exists(id: str) -> bool:
    """Check if a paper exists by ID.

    Args:
        id (str): Paper ID.

    Returns:
        bool: True if paper exists, False otherwise.
    """
    try:
        await SCHOLAR.get_paper(id, fields=["paperId"])
    except ObjectNotFoundException:
        return False

    return True


async def find_by_id(id: str) -> Paper | None:
    """Find a paper by ID.

    Args:
        id (str): Paper ID.

    Returns:
        Paper | None: Paper object if found, None otherwise.
    """
    try:
        paper = await SCHOLAR.get_paper(id)
    except ObjectNotFoundException:
        return None

    return __sanitize_paper(paper)


async def find_many_by_ids(
    ids: list[str], fields: list[str] | None = None
) -> list[Paper]:
    """Find many papers by IDs.

    Args:
        ids (list[str]): List of paper IDs.

    Returns:
        list[Paper]: List of papers.
    """
    papers = await SCHOLAR.get_papers(ids, fields=fields)
    return [__sanitize_paper(paper) for paper in papers]


async def find_many(
    query: str,
    publication_types: list[str] | None = None,
    open_access_pdf: bool = False,
    venues: list[str] | None = None,
    fields_of_study: list[UserFieldOfStudy] | None = None,
    publication_date_start: datetime | None = None,
    publication_date_end: datetime | None = None,
    min_citation_count: int | None = None,
    limit: int = 100,
    offset: int = 0,
) -> tuple[list[Paper], int]:
    """Find many papers with pagination.

    Args:
        query (str): Query to search for.
        publication_types (list[str] | None, optional): Publication types. Defaults to None.
        open_access_pdf (bool, optional): Open access PDF. Defaults to False.
        venues (list[str] | None, optional): Venues. Defaults to None.
        fields_of_study (list[UserFieldOfStudy] | None, optional): Fields of study. Defaults to None.
        publication_date_start (datetime | None, optional): Start date of publication. Defaults to None.
        publication_date_end (datetime | None, optional): End date of publication. Defaults to None.
        min_citation_count (int | None, optional): Minimum citation count. Defaults to None.
        limit (int, optional): Limit of results. Defaults to 100.
        offset (int, optional): Offset of results. Defaults to 0.

    Returns:
        tuple[list[Paper], int]: List of papers and total count.
    """
    query = __build_query(
        query,
        publication_types,
        open_access_pdf,
        venues,
        fields_of_study,
        publication_date_start,
        publication_date_end,
        min_citation_count,
    )
    url = SCHOLAR.api_url + SCHOLAR.BASE_PATH_GRAPH + "/paper/search"
    pagination = PaginatedResults(
        requester=SCHOLAR._requester,
        data_type=Paper,
        url=url,
        query=query,
        fields=Paper.SEARCH_FIELDS,
        headers=SCHOLAR.auth_header,
        limit=limit,
    )

    pagination._offset = offset - limit + 1
    pagination._next = pagination._offset + limit
    papers: list[Paper] = await pagination._async_get_next_page()

    return [__sanitize_paper(paper) for paper in papers], pagination._total


async def get_autocomplete(query: str) -> list[Autocomplete]:
    """Get autocomplete suggestions for a query.

    Args:
        query (str): Query to get autocomplete suggestions for.

    Returns:
        list[Autocomplete]: List of autocomplete suggestions.
    """
    return await SCHOLAR.get_autocomplete(query)


def __sanitize_paper(paper: Paper) -> Paper:
    """Sanitize paper object.

    Args:
        paper (Paper): Paper object.

    Returns:
        Paper: Sanitized paper object.
    """
    if not paper.openAccessPdf and paper.externalIds and paper.externalIds.get("ArXiv"):
        paper._openAccessPdf = {
            "url": f"https://arxiv.org/pdf/{paper.externalIds['ArXiv']}"
        }

    # TODO: Check the other external IDs

    return paper


def __build_query(
    query: str,
    publication_types: list[str] | None,
    open_access_pdf: bool,
    venues: list[str] | None,
    fields_of_study: list[UserFieldOfStudy] | None,
    publication_date_start: datetime | None,
    publication_date_end: datetime | None,
    min_citation_count: int | None,
) -> str:
    if publication_types:
        publication_types = ",".join(publication_types)
        query += f"&publicationTypes={publication_types}"

    query += "&openAccessPdf" if open_access_pdf else ""

    if venues:
        venues = ",".join(venues)
        query += f"&venue={venues}"

    if fields_of_study:
        fields_of_study = [__FIELD_OF_STUDY_MAP[field] for field in fields_of_study]
        fields_of_study = ",".join(fields_of_study)
        query += f"&fieldsOfStudy={fields_of_study}"

    pub_date = ""
    if publication_date_start:
        publication_date_start = publication_date_start.strftime("%Y-%m-%d")
        # from start date to today if no end date
        pub_date += f"{publication_date_start}:"

    if publication_date_end:
        publication_date_end = publication_date_end.strftime("%Y-%m-%d")
        pub_date += publication_date_end

    query += f"&publicationDateOrYear={pub_date}" if pub_date else ""

    if min_citation_count:
        query += f"&minCitationCount={min_citation_count}"

    return query


__FIELD_OF_STUDY_MAP = {
    UserFieldOfStudy.CS: "Computer Science",
    UserFieldOfStudy.MD: "Medicine",
    UserFieldOfStudy.CH: "Chemistry",
    UserFieldOfStudy.BI: "Biology",
    UserFieldOfStudy.MS: "Materials Science",
    UserFieldOfStudy.PH: "Physics",
    UserFieldOfStudy.GE: "Geology",
    UserFieldOfStudy.PS: "Psychology",
    UserFieldOfStudy.AR: "Art",
    UserFieldOfStudy.HI: "History",
    UserFieldOfStudy.GG: "Geography",
    UserFieldOfStudy.SO: "Sociology",
    UserFieldOfStudy.BU: "Business",
    UserFieldOfStudy.PO: "Political Science",
    UserFieldOfStudy.EC: "Economics",
    UserFieldOfStudy.PL: "Philosophy",
    UserFieldOfStudy.MA: "Mathematics",
    UserFieldOfStudy.EN: "Engineering",
    UserFieldOfStudy.ES: "Environmental Science",
    UserFieldOfStudy.AF: "Agricultural and Food Sciences",
    UserFieldOfStudy.ED: "Education",
    UserFieldOfStudy.LA: "Law",
    UserFieldOfStudy.LI: "Linguistics",
}
