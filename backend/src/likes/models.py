from datetime import datetime
from beanie import Document
from pydantic import BaseModel, Field
from pymongo import IndexModel


class Like(Document):
    paper_id: str
    user_id: str
    created_at: datetime = Field(default_factory=datetime.now)

    # TODO: Add info for recommendation system here?

    class Settings:
        indexes = [IndexModel([("paper_id", 1), ("user_id", 1)], unique=True)]


class LikePaperView(BaseModel):
    paper_id: str
