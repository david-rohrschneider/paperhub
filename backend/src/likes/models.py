from beanie import Document, PydanticObjectId
from pydantic import BaseModel
from pymongo import IndexModel

from src.papers.models import PaperBasicInfoView
from src.users.models import UserBasicInfoView


class Like(Document):
    paper_id: PydanticObjectId
    user_id: str
    # TODO: Add info for recommendation system here?

    class Settings:
        indexes = [IndexModel([("paper_id", 1), ("user_id", 1)], unique=True)]


class LikesWithUsersResponse(BaseModel):
    total_likes: int
    users: list[UserBasicInfoView]


class LikesWithPapersResponse(BaseModel):
    total_likes: int
    papers: list[PaperBasicInfoView]
