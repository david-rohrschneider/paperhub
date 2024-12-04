from datetime import datetime

from beanie import Document


class Comment(Document):
    user_id: str
    paper_id: str
    text: str
    created_at: datetime
