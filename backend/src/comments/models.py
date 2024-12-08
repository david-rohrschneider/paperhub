from datetime import datetime

from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field


class Comment(Document):
    user_id: str
    paper_id: PydanticObjectId
    text: str
    created_at: datetime = Field(default_factory=datetime.now)


class CommentCreateInput(BaseModel):
    paper_id: PydanticObjectId
    text: str


class CommentUpdateInput(BaseModel):
    text: str
