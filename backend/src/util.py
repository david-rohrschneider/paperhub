from src.dependencies import Pagination


def get_pagination_aggregation(
    pagination: Pagination, projection: dict[str, int | dict] | None = None
) -> list[dict]:
    data_pipeline = [
        {"$skip": pagination.offset},
        {"$limit": pagination.limit},
    ]

    if projection is not None:
        data_pipeline.append({"$project": projection})

    return [
        {
            "$facet": {
                "data": data_pipeline,
                "total": [{"$count": "count"}],
            }
        },
        {
            "$project": {
                "data": 1,
                "total": {"$ifNull": [{"$arrayElemAt": ["$total.count", 0]}, 0]},
            }
        },
    ]
